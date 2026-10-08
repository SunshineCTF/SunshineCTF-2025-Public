# docker-compose challenge (see docker-compose.yml); `pwnmake check` starts it,
# runs the solver, and tears it down.
$(call ctf_check_tcp,$(DIR),25401,python3 solve.py)

# Handouts players download (served from publish/ at /files/...)
PUBLISH += attachments/relay.py attachments/voyager.bin
