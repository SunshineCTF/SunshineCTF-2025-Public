# docker-compose challenge (see docker-compose.yml); `pwnmake check` starts it,
# runs the solver, and tears it down.
$(call ctf_check_tcp,$(DIR),25102,python3 solution/solve_headless.py)

# Handouts players download (served from publish/ at /files/...)
PUBLISH += attachments/client.py attachments/Dockerfile attachments/server
