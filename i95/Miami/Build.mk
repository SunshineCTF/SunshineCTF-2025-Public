TARGET := miami

NX := 1
ASLR := 1
RELRO := 1

DOCKER_IMAGE := sun25-i95-miami
DOCKER_PORTS := 25601
DOCKER_TIMELIMIT := 30

PUBLISH_BUILD := $(TARGET)

# `pwnmake check`: build + auto-start the PH challenge, then run the exploit and
# verify it prints flag.txt.
$(call ctf_check,$(DIR),$(DOCKER_PORTS),python3 solve.py)
