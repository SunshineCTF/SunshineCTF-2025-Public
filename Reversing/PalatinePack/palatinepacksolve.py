#!/usr/bin/env python3
import argparse

# --- Tables ---------------------------------------------------------------

SBOX = [
    0x63,0x7C,0x77,0x7B,0xF2,0x6B,0x6F,0xC5,0x30,0x01,0x67,0x2B,0xFE,0xD7,0xAB,0x76,
    0xCA,0x82,0xC9,0x7D,0xFA,0x59,0x47,0xF0,0xAD,0xD4,0xA2,0xAF,0x9C,0xA4,0x72,0xC0,
    0xB7,0xFD,0x93,0x26,0x36,0x3F,0xF7,0xCC,0x34,0xA5,0xE5,0xF1,0x71,0xD8,0x31,0x15,
    0x04,0xC7,0x23,0xC3,0x18,0x96,0x05,0x9A,0x07,0x12,0x80,0xE2,0xEB,0x27,0xB2,0x75,
    0x09,0x83,0x2C,0x1A,0x1B,0x6E,0x5A,0xA0,0x52,0x3B,0xD6,0xB3,0x29,0xE3,0x2F,0x84,
    0x53,0xD1,0x00,0xED,0x20,0xFC,0xB1,0x5B,0x6A,0xCB,0xBE,0x39,0x4A,0x4C,0x58,0xCF,
    0xD0,0xEF,0xAA,0xFB,0x43,0x4D,0x33,0x85,0x45,0xF9,0x02,0x7F,0x50,0x3C,0x9F,0xA8,
    0x51,0xA3,0x40,0x8F,0x92,0x9D,0x38,0xF5,0xBC,0xB6,0xDA,0x21,0x10,0xFF,0xF3,0xD2,
    0xCD,0x0C,0x13,0xEC,0x5F,0x97,0x44,0x17,0xC4,0xA7,0x7E,0x3D,0x64,0x5D,0x19,0x73,
    0x60,0x81,0x4F,0xDC,0x22,0x2A,0x90,0x88,0x46,0xEE,0xB8,0x14,0xDE,0x5E,0x0B,0xDB,
    0xE0,0x32,0x3A,0x0A,0x49,0x06,0x24,0x5C,0xC2,0xD3,0xAC,0x62,0x91,0x95,0xE4,0x79,
    0xE7,0xC8,0x37,0x6D,0x8D,0xD5,0x4E,0xA9,0x6C,0x56,0xF4,0xEA,0x65,0x7A,0xAE,0x08,
    0xBA,0x78,0x25,0x2E,0x1C,0xA6,0xB4,0xC6,0xE8,0xDD,0x74,0x1F,0x4B,0xBD,0x8B,0x8A,
    0x70,0x3E,0xB5,0x66,0x48,0x03,0xF6,0x0E,0x61,0x35,0x57,0xB9,0x86,0xC1,0x1D,0x9E,
    0xE1,0xF8,0x98,0x11,0x69,0xD9,0x8E,0x94,0x9B,0x1E,0x87,0xE9,0xCE,0x55,0x28,0xDF,
    0x8C,0xA1,0x89,0x0D,0xBF,0xE6,0x42,0x68,0x41,0x99,0x2D,0x0F,0xB0,0x54,0xBB,0x16
]
INV_SBOX = [0]*256
for i,v in enumerate(SBOX):
    INV_SBOX[v] = i

# --- Bit rotations across a small byte block (little-endian packing) -----

def rotate_block_left(block: bytearray, bits: int) -> None:
    n = len(block)
    if n == 0 or bits % (n*8) == 0: return
    total = 0
    for i, b in enumerate(block):
        total |= (b & 0xFF) << (8*i)
    mask = (1 << (n*8)) - 1
    bits %= (n*8)
    total = ((total << bits) | (total >> ((n*8)-bits))) & mask
    for i in range(n):
        block[i] = (total >> (8*i)) & 0xFF

def rotate_block_right(block: bytearray, bits: int) -> None:
    n = len(block)
    if n == 0 or bits % (n*8) == 0: return
    total = 0
    for i, b in enumerate(block):
        total |= (b & 0xFF) << (8*i)
    mask = (1 << (n*8)) - 1
    bits %= (n*8)
    total = ((total >> bits) | (total << ((n*8)-bits))) & mask
    for i in range(n):
        block[i] = (total >> (8*i)) & 0xFF

# --- The “weird” layer and its true inverse (fixed vs the C comment) -----

def doWeirdStuff(buf: bytearray) -> None:
    BS = 5
    for i in range(0, len(buf), BS):
        block = buf[i:i+BS]
        remain = len(block)
        # per-byte SBOX after XOR with j
        for j in range(remain):
            block[j] = SBOX[block[j] ^ j]
        # rotate left by remain*3 bits across the block
        rotate_block_left(block, remain * 3)
        buf[i:i+BS] = block

def deweird(buf: bytearray) -> None:
    BS = 5
    for i in range(0, len(buf), BS):
        block = bytearray(buf[i:i+BS])
        remain = len(block)
        # inverse rotation first
        rotate_block_right(block, remain * 3)
        # inverse of y = SBOX[x ^ j]  =>  x = INV_SBOX[y] ^ j
        for j in range(remain):
            block[j] = INV_SBOX[block[j]] ^ j
        buf[i:i+BS] = block

# --- expand / deexpand (case 1 in your switch; shift_key value irrelevant) ---

def deexpand(buf: bytes) -> bytearray:
    """Invert the expand() case-1 logic (no weird layer here)."""
    assert len(buf) % 2 == 0, "deexpand expects length divisible by 2"
    out = bytearray(len(buf)//2)
    shift = 0
    # shift_key multiplies by 11 each input byte in C, but it never affects
    # the recovered nibble because we AND back the original nibbles.
    for i in range(len(out)):
        b0 = buf[2*i]
        b1 = buf[2*i + 1]
        if shift == 0:
            recovered = (b1 & 0xF0) | (b0 & 0x0F)
        else:
            recovered = (b0 & 0xF0) | (b1 & 0x0F)
        out[i] = recovered
        shift ^= 1
    return out

# flipBits is an involution (apply again to undo)
def flipBits(buf: bytearray) -> None:
    flip = 0
    xor_key = 0x69
    for i in range(len(buf)):
        if flip == 0:
            buf[i] = (~buf[i]) & 0xFF
        else:
            buf[i] ^= xor_key
            xor_key = (xor_key + 0x420) & 0xFF
        flip ^= 1

# --- High-level decrypt ---------------------------------------------------

def decrypt(cipher: bytes, apply_weird: bool) -> bytes:
    data = bytearray(cipher)

    # If the producer had doWeirdStuff enabled, undo it first (it ran after each expand).
    # In your current C, doWeirdStuff is commented out, so this is off unless --weird is passed.
    if apply_weird:
        deweird(data)                 # undo weird after 3rd expand
    data = deexpand(data)             # 3 -> 2
    if apply_weird:
        deweird(data)
    data = deexpand(data)             # 2 -> 1
    if apply_weird:
        deweird(data)
    data = deexpand(data)             # 1 -> 0 (original length)
    # flipBits to finish (it’s self-inverse)
    flipBits(data)
    return bytes(data)

# --- CLI ------------------------------------------------------------------

def main():
    p = argparse.ArgumentParser(description="Decrypt output from the C packer (expand×3 [+ weird?] + flipBits).")
    p.add_argument("-i", "--infile", required=True, help="input file (the packer's output; e.g. flag.txt)")
    p.add_argument("-o", "--outfile", default="decrypted.txt", help="where to write plaintext")
    p.add_argument("--weird", action="store_true",
                   help="set if your build ENABLED doWeirdStuff() during packing (default: off)")
    args = p.parse_args()

    with open(args.infile, "rb") as f:
        ct = f.read()

    # Sanity: length after triple expand should be 8× original ⇒ divisible by 8
    if len(ct) % 8 != 0:
        print(f"[!] Warning: input length {len(ct)} is not divisible by 8. Proceeding anyway.")

    pt = decrypt(ct, apply_weird=args.weird)

    with open(args.outfile, "wb") as f:
        f.write(pt)

    try:
        print(pt.decode(errors="replace"))
    except Exception:
        pass
    print(f"[+] Wrote plaintext to {args.outfile}")

if __name__ == "__main__":
    main()
