# rover_client_full.py
import sys, socket, json, threading, queue, time, struct
import pygame

WIDTH, HEIGHT = 900, 600
BG = (8, 10, 16)
FG = (230, 235, 240)
TRACK_CLR = (40, 40, 48)
FINISH_CLR = (220, 220, 220)
ROVER_CLR = (120, 200, 255)
OBST_CLR = (255, 120, 120)

# Vertical scroll scale: pixels per world-unit ahead
PX_PER_WU = 2.2

def pack_can_hex(can_id: int, data: bytes) -> str:
    """Pack CAN frame: [ID_hi][ID_lo][DLC][DATA...] -> hex string."""
    can_id &= 0x7FF
    frame = bytes([(can_id >> 8) & 0xFF, can_id & 0xFF, len(data) & 0x0F]) + data
    return frame.hex()

class Net:
    def __init__(self, host, port):
        self.sock = socket.create_connection((host, port))
        # line-buffered text files for NDJSON
        self.r = self.sock.makefile('r', buffering=1, encoding='utf-8', newline='\n')
        self.w = self.sock.makefile('w', buffering=1, encoding='utf-8', newline='\n')
        self.q = queue.Queue()
        self.alive = True
        threading.Thread(target=self.reader, daemon=True).start()

    def reader(self):
        try:
            for line in self.r:
                line = line.strip()
                if not line:
                    continue
                try:
                    obj = json.loads(line)
                    self.q.put(obj)
                except Exception:
                    # Ignore malformed lines
                    pass
        except Exception:
            pass
        self.alive = False

    def send_can(self, can_id: int, data: bytes):
        """Send a CAN frame (as hex) wrapped in JSON: {"t":"can","frame":...}"""
        try:
            frame_hex = pack_can_hex(can_id, data)
            msg = {"t": "can", "frame": frame_hex}
            self.w.write(json.dumps(msg) + "\n")
            self.w.flush()
        except Exception:
            self.alive = False

def world_to_screen_x(x_wu, half_width_wu, rover_x=0.0):
    """
    Map world x in [-half,+half] (after shifting the world by rover_x so rover stays centered)
    to screen x in [WIDTH*0.2, WIDTH*0.8].
    """
    left = WIDTH * 0.2
    right = WIDTH * 0.8
    x_rel = float(x_wu) - float(rover_x)  # shift the world under the rover
    t = (x_rel + half_width_wu) / (2 * half_width_wu)
    return int(left + t * (right - left))

def main():
    if len(sys.argv) != 3:
        print(f"usage: python {sys.argv[0]} HOST PORT")
        sys.exit(1)
    host, port = sys.argv[1], int(sys.argv[2])

    net = Net(host, port)

    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Space Race: Rover (Tester Client)")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 20)
    big = pygame.font.SysFont(None, 48)

    # Optional: enable key repeat so holding arrows adjusts continuously
    pygame.key.set_repeat(200, 80)

    latest = None
    flag = None
    flag_time = None

    # Local control state we send; we also keep an eye on server-echoed values
    throttle = 0      # 0..100
    steer = 0         # -100..100

    def set_throttle(val):
        nonlocal throttle
        throttle = max(0, min(100, int(val)))
        net.send_can(0x201, bytes([throttle]))

    def set_steer(val):
        nonlocal steer
        steer = max(-100, min(100, int(val)))
        net.send_can(0x202, struct.pack("b", steer))

    while True:
        # Receive telemetry
        try:
            while True:
                obj = net.q.get_nowait()
                if obj.get("t") == "telemetry":
                    latest = obj
                    # Keep local HUD in sync with server values (when present)
                    throttle = int(latest.get("throttle_pct", throttle))
                    steer = int(latest.get("steer_pct", steer))
                    if obj.get("flag") is not None and flag is None:
                        flag = obj["flag"]
                        flag_time = time.time()
        except queue.Empty:
            pass

        # Input
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit(); return
            if e.type == pygame.KEYDOWN:
                if e.key in (pygame.K_ESCAPE, pygame.K_q):
                    pygame.quit(); return
                elif e.key == pygame.K_UP:
                    set_throttle(throttle + 5)
                elif e.key == pygame.K_DOWN:
                    set_throttle(throttle - 5)
                elif e.key == pygame.K_LEFT:
                    set_steer(steer - 10)
                elif e.key == pygame.K_RIGHT:
                    set_steer(steer + 10)
                elif e.key == pygame.K_b:
                    net.send_can(0x203, b"")     # brake
                elif e.key == pygame.K_s:
                    set_steer(0)
                    net.send_can(0x204, b"")     # stabilize
                elif e.key == pygame.K_r:
                    net.send_can(0x205, b"")     # reset

        # Draw
        screen.fill(BG)

        if latest:
            track = latest.get("track", {})
            half_w = float(track.get("half_width", 60.0))
            rover_x = float(latest.get("x", 0.0))
            # Track edges should shift horizontally with rover_x
            tlx = world_to_screen_x(-half_w, half_w, rover_x)
            trx = world_to_screen_x(+half_w, half_w, rover_x)
            track_px_w = max(1, trx - tlx)

            # Track area
            pygame.draw.rect(screen, TRACK_CLR, (tlx, 0, track_px_w, HEIGHT), border_radius=12)

            # Finish hint near the right boundary when close to finish
            s = float(latest.get("s", 0.0))
            length = float(track.get("length", 1.0))
            progress = s / max(1.0, length)
            if progress > 0.85:
                for y in range(0, HEIGHT, 14):
                    pygame.draw.line(screen, FINISH_CLR, (trx, y), (trx, y+7), 3)

            # Obstacles (scrolling): dy = distance AHEAD; rover is centered vertically
            obs = latest.get("obstacles", [])
            if obs is not None:
                for ob in obs:
                    try:
                        dy = float(ob["dy"])
                        if dy < 0:
                            continue
                        y = int(HEIGHT/2 - dy * PX_PER_WU)
                        x = world_to_screen_x(float(ob["x"]), half_w, rover_x)
                        # Obstacle width scaled by track visible width
                        w_px = max(6, int((float(ob["w"]) / (2 * half_w)) * track_px_w))
                        rect = pygame.Rect(x - w_px//2, y - 10, w_px, 20)
                        pygame.draw.rect(screen, OBST_CLR, rect, border_radius=4)
                    except (KeyError, ValueError, TypeError):
                        # Skip malformed obstacle entries
                        continue

            # Rover fixed at screen center (simple rectangle)
            rover_rect = pygame.Rect(WIDTH//2 - 16, HEIGHT//2 + 18, 32, 44)
            pygame.draw.rect(screen, ROVER_CLR, rover_rect, border_radius=6)
            pygame.draw.rect(screen, FG, rover_rect, 2, border_radius=6)

            # HUD
            hud = [
                f"Status: {latest.get('status','')}",
                f"Dist: {s:.1f}/{length:.0f} wu",
                f"Lateral x: {rover_x:.1f} wu",
                f"Speed: {float(latest.get('vel',0.0)):.2f} wu/s",
                f"Throttle: {latest.get('throttle_pct',0)}%  Steer: {latest.get('steer_pct',0)}%",
                f"Msg: {str(latest.get('msg',''))[:64]}",
                "Controls: ↑/↓ throttle, ←/→ steer, B brake, S stabilize, R reset, Q/Esc quit",
            ]
            for i, line in enumerate(hud):
                img = font.render(line, True, FG)
                screen.blit(img, (12, 10 + i*18))

        # Flag overlay
        if flag:
            img = big.render(flag, True, (255, 240, 120))
            screen.blit(img, img.get_rect(center=(WIDTH//2, HEIGHT//2 - 80)))

        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()
