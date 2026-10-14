#!/bin/bash
# Runs during pwnmake image initialization. Installs the python modules the
# challenge solver scripts need so `pwnmake check` can run them in the container.
# Most 2025 solvers use only pwntools, requests, and the Python stdlib.
#
# binutils-aarch64-linux-gnu provides the cross `as`/`ld`/`objcopy` and `cpp`
# the C preprocessor, both of which pwntools needs to assemble the arm64
# shellcode in i95/Daytona's solver. xz-utils lets `pwnmake publish` unpack
# Reversing/Warp's handout (kept xz-compressed in git) for players.
set -e
apt-get update
apt-get install -y --no-install-recommends \
	python3-pwntools \
	python3-requests \
	binutils-aarch64-linux-gnu \
	cpp \
	xz-utils

# docker compose v2 plugin + a `docker-compose` shim, so `pwnmake` can bring the
# docker-compose challenges up/down from inside the pwnmake container (used by the
# compose check macros' auto-start/teardown).
COMPOSE_VERSION=v2.29.7
PLUGIN_DIR=/usr/libexec/docker/cli-plugins
mkdir -p "$PLUGIN_DIR"
if [ ! -x "$PLUGIN_DIR/docker-compose" ]; then
	curl -fsSL "https://github.com/docker/compose/releases/download/${COMPOSE_VERSION}/docker-compose-linux-x86_64" \
		-o "$PLUGIN_DIR/docker-compose"
	chmod +x "$PLUGIN_DIR/docker-compose"
fi
cat > /usr/local/bin/docker-compose <<'SH'
#!/bin/sh
exec docker compose "$@"
SH
chmod +x /usr/local/bin/docker-compose
