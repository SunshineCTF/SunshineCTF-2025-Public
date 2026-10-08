#!/usr/bin/env python3
"""
Headless autopilot solver for Space Race.

The intended solve is to reverse the CAN protocol used by the rover ECU and
implement the controls (throttle 0x201, steering 0x202, brake 0x203,
stabilize 0x204, reset 0x205) to drive the rover to the finish line while
dodging obstacles. The provided solution/client.py is an interactive PyGame
tester; this script is the same protocol driven by a simple autopilot so the
solve can be verified without a human/display.

Usage: python3 solve_headless.py HOST PORT
"""
import os, sys, socket, json, time

TRACK_HALF = 60.0
ROVER_W = 10.0


def pack_can_hex(can_id: int, data: bytes) -> str:
    can_id &= 0x7FF
    frame = bytes([(can_id >> 8) & 0xFF, can_id & 0xFF, len(data) & 0x0F]) + data
    return frame.hex()


def main():
    host = os.environ.get("HOST") or (sys.argv[1] if len(sys.argv) > 1 else "localhost")
    port = int(os.environ.get("PORT") or (sys.argv[2] if len(sys.argv) > 2 else 25102))

    sock = socket.create_connection((host, port))
    r = sock.makefile("r", buffering=1, encoding="utf-8", newline="\n")
    w = sock.makefile("w", buffering=1, encoding="utf-8", newline="\n")

    def send_can(cid, data=b"\x00"):
        w.write(json.dumps({"t": "can", "frame": pack_can_hex(cid, data)}) + "\n")
        w.flush()

    def throttle(pct):
        send_can(0x201, bytes([max(0, min(100, int(pct)))]))

    def steer(pct):
        send_can(0x202, bytes([int(pct) & 0xFF]))  # int8

    def brake():
        send_can(0x203)

    def reset():
        send_can(0x205)

    deadline = time.time() + 90
    while time.time() < deadline:
        line = r.readline()
        if not line:
            break
        line = line.strip()
        if not line:
            continue
        try:
            tel = json.loads(line)
        except Exception:
            continue
        if tel.get("flag"):
            print("FLAG:", tel["flag"])
            return 0
        status = tel.get("status")
        if status == "finished":
            # flag arrives on the same or next telemetry frame
            continue
        if status == "crashed":
            reset()
            throttle(0)
            continue

        x = tel.get("x", 0.0)
        vel = tel.get("vel", 0.0)
        obstacles = tel.get("obstacles", []) or []

        # Pick a target lateral position that avoids the nearest obstacle ahead.
        target_x = 0.0
        nearest = None
        for ob in obstacles:
            if ob.get("dy", 1e9) >= 0:
                if nearest is None or ob["dy"] < nearest["dy"]:
                    nearest = ob
        if nearest is not None and nearest["dy"] < 120:
            ow = nearest["w"]
            ox = nearest["x"]
            # Gap on the left vs right of the obstacle; pick the side with more room.
            left_room = (ox - ow / 2) - (-TRACK_HALF + ROVER_W / 2)
            right_room = (TRACK_HALF - ROVER_W / 2) - (ox + ow / 2)
            if left_room >= right_room:
                target_x = ox - ow / 2 - ROVER_W / 2 - 2
            else:
                target_x = ox + ow / 2 + ROVER_W / 2 + 2
            target_x = max(-TRACK_HALF + ROVER_W / 2, min(TRACK_HALF - ROVER_W / 2, target_x))

        # Proportional steering toward target_x.
        err = target_x - x
        sp = max(-100, min(100, int(err * 12)))
        steer(sp)

        # Keep speed modest so there is time to react to obstacles.
        if nearest is not None and nearest["dy"] < 40 and abs(err) > 4:
            throttle(15)
        elif vel > 22:
            throttle(10)
        else:
            throttle(45)

    print("Did not finish in time")
    return 1


if __name__ == "__main__":
    sys.exit(main())
