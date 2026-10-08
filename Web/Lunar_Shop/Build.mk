# docker-compose challenge (see docker-compose.yml); `pwnmake check` starts it,
# runs the solver, and tears it down.
$(call ctf_check_web,$(DIR),25306,lunarshop.ctf.hackucf.org,python3 solve.py)
