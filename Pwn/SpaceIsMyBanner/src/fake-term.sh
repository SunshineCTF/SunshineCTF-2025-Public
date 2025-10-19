#!/bin/sh
trap 'exit 1' SIGINT

# set up a private session to avoid annoying fellow competitors
export SHELL=/app/challenge.sh
export TERM=xterm
export TMUX_TMPDIR=$(mktemp -d)

tmux new-session -D -f /etc/tmux.conf -s secret-session

# clean up the dead socket if a user exits. swallow errors
/usr/bin/find /tmp  -path '/tmp/tmp.*' -user $(id -u) -delete &>/dev/null