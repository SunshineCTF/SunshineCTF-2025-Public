from pwn import *
from binascii import hexlify, unhexlify

# Connect to the challenge
S = remote("localhost", 1337)
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
    KS = bytearray([x^y for x,y in zip(PT,CT)])

    # Add this to known keystream
    KEYSTREAM += KS

    # XOR collected keystream blocks with first complete message
    print(bytearray([x^y for x,y in zip(MESSAGE,KEYSTREAM)]).decode())
