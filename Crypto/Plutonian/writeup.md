# Plutonian Crypto

## Crypto (Easy/Medium)

## Solution

AES-CTR mode generates a keystream which is XOR'd with blocks of plaintext. However, since the same nonce is reused and then the initial counter variable is incremented with each message, the keystream is the same but just shifts one block to the left each time. This means that, because we know at least the first 16 characters of the message, we can save the very first message, and then XOR the first block of every subsequent message with the known plaintext. Once we have collected enough blocks, we can XOR them with the first message, revealing the complete plaintext message.

```python
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

```