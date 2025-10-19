# [RE] Numbers Game
### Author: Kyle Cahalan

Docker and pwnmake are required to run the challenge as intended, but you can live without. Compiling the challenge from main.c using gcc and running the exe from that should work fine.

Build and run challenge then connect to it:
```bash
pwnmake docker-start
nc localhost 25101
```

Writeup:
```bash
./numbers-game-writeup.md
```

Solver:
```bash
python3 ./solver/solver.pwntools.py
```

