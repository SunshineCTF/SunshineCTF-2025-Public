#!/usr/bin/env python3
POOP = "💩"
ZWSP = "\u200b"

with open("poop_challenge.txt", "r", encoding="utf-8") as f:
    s = f.read()

bits = []
i = 0
n = len(s)
while i < n:
    ch = s[i]
    if ch == POOP:
        # Look ahead for ZWSP
        if i + 1 < n and s[i+1] == ZWSP:
            bits.append("1")
            i += 2
        else:
            bits.append("0")
            i += 1
    else:
        # skip newlines or any other stray chars
        i += 1

# group into bytes
out = []
for j in range(0, len(bits), 8):
    byte = bits[j:j+8]
    if len(byte) < 8:
        break
    out.append(chr(int("".join(byte), 2)))
print("".join(out))
