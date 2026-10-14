# docker-compose challenge (see docker-compose.yml).
#
# The intended solution needs outbound internet access (public DNS and a publicly
# reachable server), so it cannot run in the offline check sandbox. solve.py is
# env-driven for live use, but the check is left commented out so `pwnmake check`
# does not always fail here.
#
# $(call ctf_check_web,$(DIR),25304,webhook.ctf.hackucf.org,python3 solve.py)

# The check is disabled above, so publish the nginx snippet directly.
$(call nginx_service,webhook.ctf.hackucf.org,25304)
