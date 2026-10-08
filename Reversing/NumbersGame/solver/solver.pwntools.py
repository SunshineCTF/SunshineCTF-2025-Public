#!/usr/bin/env python3
from pwn import *
import subprocess

result = subprocess.run(
        "./solver/parallel-generator | .build/Reversing/NumbersGame/numbers-game",
        shell=True,
        cwd=".",
        capture_output=True,
        text=True
)

for line in result.stdout.splitlines():
    if "{" in line:
        print(line)
        break

