TARGET := clone_army

SRCS := clone_army.c

# This is super important for this challenge.
ASLR := 0

# RELRO must stay disabled for this challenge.
RELRO := 0

NX := 1
CANARY := 1

# Be a little nice to the players...
STRIP := 0

# ...but not TOO nice :)
DEBUG := 0


# Publish the binary as well as libc and ld.
PUBLISH_BUILD := $(TARGET)
PUBLISH_LIBC := clone_army-libc.so
PUBLISH_LD := clone_army-ld.so


DOCKER_IMAGE := sun25-clone-army
DOCKER_PORTS := 25001
DOCKER_TIMELIMIT := 30
DOCKER_BUILD_ARGS := --build-arg DIR=$(DIR)

# `pwnmake check`: build + auto-start the PH challenge, run the exploit and
# verify it prints the flag.
$(call ctf_check,$(DIR),$(DOCKER_PORTS),python3 solve.py)
