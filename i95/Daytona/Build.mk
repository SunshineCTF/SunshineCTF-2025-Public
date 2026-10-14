# docker-compose challenge (arm64 under QEMU; see docker-compose.yml). The host
# needs QEMU binfmt support for arm64 registered (see README.md).
# `pwnmake check` starts it, runs the solver, and tears it down.
$(call ctf_check_tcp,$(DIR),25606,python3 solve.py)

# pwnmake exports DOCKER_DEFAULT_PLATFORM=linux/amd64 for its own image, and
# docker compose refuses to build a service whose `platform: linux/arm64`
# disagrees with it ("build.platforms does not support value set by
# DOCKER_DEFAULT_PLATFORM"). Match the default to the service for the compose
# targets that may build (`up -d` builds a missing image).
docker-rebuild-one[$(DIR)] docker-start-one[$(DIR)]: DOCKER_DEFAULT_PLATFORM := linux/arm64

# Handouts players download (served from publish/ at /files/...)
PUBLISH += daytona
