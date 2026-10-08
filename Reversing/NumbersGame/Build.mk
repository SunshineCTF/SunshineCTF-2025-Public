TARGETS := numbers-game solve

NX := 1
ASLR := 1
# RELRO := 1
# CANARY := 1
# STRIP := 1
# DEBUG := 1

numbers-game_SRCS := main.c
solve_SRCS := solve.c

PUBLISH_BUILD := $(firstword $(TARGETS))

DOCKER_IMAGE := sun25-numbers-game
DOCKER_PORTS := 25101
DOCKER_TIMELIMIT := 30

# `pwnmake check`: build + auto-start the PH challenge, run the solver and
# verify it prints the flag.
$(call ctf_check,$(DIR),$(DOCKER_PORTS),python3 solve.py)
