TARGET := jupiter-2025
# Unique target name (distinct from 2024's i95/jupiter); keep the clean
# runtime/connect name:
DOCKER_CHALLENGE_NAME := jupiter
NX := 1
RELRO := 1
CANARY := 1

DOCKER_IMAGE := sun25-i95-jupiter
DOCKER_PORTS := 25607
DOCKER_TIMELIMIT := 30

PUBLISH_BUILD := $(TARGET)

# `pwnmake check`: build + auto-start the PH challenge, then run the exploit and
# verify it prints flag.txt.
$(call ctf_check,$(DIR),$(DOCKER_PORTS),python3 solve.py)
