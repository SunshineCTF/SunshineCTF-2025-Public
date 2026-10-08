#!/usr/bin/env python3
# Plutonian solver.
#
# The station re-encrypts the same plaintext each round with AES-CTR, nonce
# fixed and the starting counter incremented by one per message. So the first
# 16-byte block of message C is encrypted with keystream block C. Knowing the
# first 16 plaintext bytes ("Greetings, Earth") recovers one keystream block per
# message; collecting enough of them lets us decrypt the whole first message,
# whose tail contains the flag.
import os
import re
import sys
from pwn import remote
from binascii import unhexlify

HOST = os.environ.get("HOST", "localhost")
PORT = int(os.environ.get("PORT", 25403))

# Connect to the challenge
S = remote(HOST, PORT)
S.recvuntil(b"BEGINNING TRANSMISSION ==\n\n")  # Skip ASCII art

# Known first block of plaintext (16 characters)
PT = b"Greetings, Earth"

KEYSTREAM = b''

# We save the first message to decode later
MESSAGE = None

while True:

    # Get a ciphertext
    CT = S.recvline().decode().strip()

    # Save first message to decode with captured keystream blocks
    if MESSAGE is None:
        MESSAGE = unhexlify(CT)

    # Convert first block from hex
    CT = unhexlify(CT[:32])

    # XOR with known plaintext
    KS = bytearray([x ^ y for x, y in zip(PT, CT)])

    # Add this to known keystream
    KEYSTREAM += KS

    # XOR collected keystream blocks with first complete message
    decoded = bytes([x ^ y for x, y in zip(MESSAGE, KEYSTREAM)])
    print(decoded.decode(errors="replace"))

    # Once enough keystream is recovered the flag at the tail appears.
    m = re.search(rb"sun\{[^}]*\}", decoded)
    if m:
        print(m.group(0).decode())
        break

S.close()
