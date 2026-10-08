# Space Race

## Reverse Engineering / Scripting

The player is given some skeleton PyGame code to visualize the race along with the rover server binary.

## Deployment

The server component can be deployed by building the Dockerfile in src/server

```bash
docker build -t space-race .
docker run -p 1337:1337 space-race
```

See [writeup.md](writeup.md) for the solution.
