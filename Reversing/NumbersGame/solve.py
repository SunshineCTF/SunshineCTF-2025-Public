#!/usr/bin/env python3
# Numbers Game solver (server edition).
#
# The challenge seeds glibc's rand() with time(NULL) and asks us to guess the
# 64-bit value built from three rand() calls. We recreate the exact same
# computation with solver/parallel-generator.c (compiled against the same glibc
# rand()), so as long as we generate our guess in the same wall-clock second the
# server seeded, we predict its number and it cats the flag. A short retry loop
# absorbs the rare case where we straddle a second boundary.
import os
import subprocess
from pwn import *

HOST = os.environ.get("HOST", "localhost")
PORT = int(os.environ.get("PORT", 25101))

_HERE = os.path.dirname(os.path.abspath(__file__))
GEN = os.path.join(_HERE, "solver", "parallel-generator")
SRC = os.path.join(_HERE, "solver", "parallel-generator.c")

# Build the predictor if the (gitignored) binary isn't present.
if not os.path.exists(GEN):
	subprocess.run(["gcc", "-O2", SRC, "-o", GEN], check=True)

context.log_level = "warn"


def attempt():
	r = remote(HOST, PORT)
	# Generate the guess as close as possible to when the server called srand().
	guess = subprocess.check_output([GEN]).strip()
	r.sendline(guess)
	data = r.recvall(timeout=5)
	r.close()
	return data


for i in range(16):
	data = attempt()
	if b"sun{" in data:
		print(data.decode(errors="replace"))
		break
else:
	print("Failed to predict the number after several attempts.")
	print(data.decode(errors="replace"))
