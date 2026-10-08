TARGET := heapx

NX := 1
ASLR := 1
RELRO := 1
CANARY := 1
STRIP := 1

GLIBC_VERSION := 2.41

PUBLISH_BUILD := $(TARGET)
PUBLISH_LIBC := libc.so.6
PUBLISH_LD := ld-linux-x86-64.so.2 

DOCKER_IMAGE := sun25-heapx
DOCKER_PORTS := 25004
DOCKER_TIMELIMIT := 30

# `pwnmake check`: build + auto-start the PH challenge, run the exploit and
# verify it prints the flag.
$(call ctf_check,$(DIR),$(DOCKER_PORTS),python3 solve.py)
