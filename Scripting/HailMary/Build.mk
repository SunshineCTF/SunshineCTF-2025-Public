# docker-compose challenge (see docker-compose.yml). The solver can take a long
# time to finish, so give it more time than the default.
CHECK_TIMEOUT := 600
# `pwnmake check` starts it, runs the solver, and tears it down.
$(call ctf_check_tcp_slow,$(DIR),25201,python3 solve.py)
