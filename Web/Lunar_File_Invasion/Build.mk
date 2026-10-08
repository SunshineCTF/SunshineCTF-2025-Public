# docker-compose challenge (see docker-compose.yml); `pwnmake check` starts it,
# runs the solver, and tears it down.
$(call ctf_check_web,$(DIR),25307,lunarfileinvasion.ctf.hackucf.org,python3 solve.py)
