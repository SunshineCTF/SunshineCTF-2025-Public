#!/usr/bin/env python3
# BitsOfSpace solver.
#
# The relay authorizes by decrypting a 48-byte AES-CBC subscription packet and
# checking the device_id in the first plaintext block. Because CBC's first
# plaintext block is AES-DEC(C0) XOR IV, we can flip the device_id from the
# issued 0x13371337 to the restricted 0xdeadbabe *without* the key by XORing the
# difference into the first 4 IV bytes. Sending the tampered packet makes the
# relay hand us the flag.
#
# Pure stdlib (XOR only) so the check needs no extra python packages.
import os
import struct
from pwn import remote

BLOCK = 16

HOST = os.environ.get("HOST", "localhost")
PORT = int(os.environ.get("PORT", 25401))

_HERE = os.path.dirname(os.path.abspath(__file__))


def flip_device_id(data: bytes, old_id: int, new_id: int) -> bytes:
    iv = bytearray(data[:BLOCK])
    body = data[BLOCK:]

    old_bytes = struct.pack("<I", old_id)
    new_bytes = struct.pack("<I", new_id)

    # device_id is block[0], offset 0..3 -> flip the matching IV bytes.
    for i in range(4):
        iv[i] ^= old_bytes[i] ^ new_bytes[i]

    return bytes(iv) + body


def main():
    with open(os.path.join(_HERE, "attachments", "voyager.bin"), "rb") as f:
        original = f.read()

    modified = flip_device_id(original, 0x13371337, 0xdeadbabe)

    r = remote(HOST, PORT)
    r.send(modified)
    print(r.recvall(timeout=5).decode(errors="replace"))


if __name__ == "__main__":
    main()
