#!/bin/sh
trap 'exit 1' SIGINT
export TERM=xterm
exec /app/challenge.sh
