# docker-compose challenge (arm64 under QEMU; see docker-compose.yml). The host
# needs QEMU binfmt support for arm64 registered (see README.md).
# `pwnmake check` starts it, runs the solver, and tears it down.
$(call ctf_check_tcp,$(DIR),25606,python3 solve.py)

# Handouts players download (served from publish/ at /files/...)
PUBLISH += daytona
