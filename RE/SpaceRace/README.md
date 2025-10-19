# Space Race

## Reverse Engineering / Scripting

This challenge is focused on interacting with vehicle networks using CANBUS to communicate. The onboard rover software has various arbitration IDs that it uses to determine different parameters about the vehicle. The player is given some skeleton PyGame code to visualize the race but has to actually implement the rest of the communications themselves by reverse engineering the provided binary.

## Deployment

The server component can be deployed by building the Dockerfile in src/server

```bash
docker build -t space-race .
docker run -p 1337:1337 space-race
```
