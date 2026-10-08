TARGET := jacksonville-2025
# Unique target name (distinct from 2024's i95/jacksonville); keep the clean
# runtime/connect name:
DOCKER_CHALLENGE_NAME := jacksonville
NX := 1
RELRO := 1

DOCKER_IMAGE := sun25-i95-jacksonville
DOCKER_PORTS := 25602
DOCKER_TIMELIMIT := 30

PUBLISH_BUILD := $(TARGET)

# `pwnmake check`: build + auto-start the PH challenge, then run the exploit and
# verify it prints flag.txt.
$(call ctf_check,$(DIR),$(DOCKER_PORTS),python3 solve.py)
