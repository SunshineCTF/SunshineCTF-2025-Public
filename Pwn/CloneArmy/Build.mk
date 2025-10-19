TARGET := clone_army

SRCS := clone_army.c

# This is super important for this challenge, as the binary must be loaded
# at a 32-bit address (top 32 bits zero), and there's no intentional info leak
# (before corruption) to find the base address of the binary.
ASLR := 0

# Intended exploit overwrites a GOT entry, so we need to disable RELRO.
RELRO := 0

NX := 1
CANARY := 1

# Be a little nice to the players...
STRIP := 0

# ...but not TOO nice :)
DEBUG := 0


# Publish the binary as well as libc and ld.
# The intended exploit needs to figure out the offset between different
# functions within libc.
PUBLISH_BUILD := $(TARGET)
PUBLISH_LIBC := clone_army-libc.so
PUBLISH_LD := clone_army-ld.so


DOCKER_IMAGE := clone-army
DOCKER_PORTS := 25001
DOCKER_TIMELIMIT := 30
DOCKER_BUILD_ARGS := --build-arg DIR=$(DIR)
