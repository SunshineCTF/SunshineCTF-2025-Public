#!/bin/bash

echo "Hi from wrapper.sh"

# 512 MiB virtual memory limit
ulimit -v 524288

exec /home/clone_army/clone_army
