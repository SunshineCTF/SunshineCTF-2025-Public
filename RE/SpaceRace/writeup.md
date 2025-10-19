# Space Race

## Reverse Engineering / Scripting

In order to steer the vehicle to avoid obstacles and also increase the speed, the player needs to look for this block in the provided client code:

```python
for e in pygame.event.get():
    if e.type == pygame.QUIT:
        pygame.quit(); return
    if e.type == pygame.KEYDOWN:
        if e.key in (pygame.K_ESCAPE, pygame.K_q):
            pygame.quit(); return
        elif e.key == pygame.K_UP:
            pass
        elif e.key == pygame.K_DOWN:
            pass
        elif e.key == pygame.K_LEFT:
            pass
        elif e.key == pygame.K_RIGHT:
            pass
        elif e.key == pygame.K_b:
            pass
        elif e.key == pygame.K_s:
            pass
        elif e.key == pygame.K_r:
            pass
```

They can add functions to each of these to send the correct CANBUS packets to be able to steer the vehicle, which they need to discover by reverse engineering the binary. Once they do this they will discover the IDs needed:

We can see these in the Golang source which they will not receive.

```golang
case 0x201: // throttle
    ~if dlc >= 1 {
        rover.throttlePct = clampInt(int(data[0]), 0, 100)
        rover.msg = fmt.Sprintf("Throttle %d%%", rover.throttlePct)
    }
case 0x202: // steering
    if dlc >= 1 {
        sp := int(int8(data[0]))
        rover.steerPct = clampInt(sp, -100, 100)
        rover.msg = fmt.Sprintf("Steer %d%%", rover.steerPct)
    }
case 0x203: // brake
    rover.vel *= brakeFactor
    rover.msg = "Brake!"
case 0x204: // stabilize
    rover.steerPct = 0
    rover.heading *= 0.9
    rover.msg = "Stabilizers on"
case 0x205: // reset
    if rover.status != "ok" {
        rover.s, rover.x, rover.vel = 0, 0, 0
        rover.throttlePct, rover.steerPct = 0, 0
        rover.status = "ok"
        rover.msg = "Reset to start"
    }
```

Once these CANBUS packets are properly implemented, the player will be able to simply start the client and drive forward, avoiding obstacles, till they get to the end and get the flag!

See [solution/client.py](solution/client.py) for a working version.