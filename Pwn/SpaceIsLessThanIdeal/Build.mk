# docker-compose challenge (see docker-compose.yml); `pwnmake check` starts it,
# runs the solver, and tears it down.
$(call ctf_check_tcp,$(DIR),25003,bash solve.sh)
