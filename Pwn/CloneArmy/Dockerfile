FROM c0deh4cker/pwnableharness:base-24.04-v2.1

ARG DIR
COPY "$DIR/wrapper.sh" /home/clone_army/wrapper.sh

ENTRYPOINT [ \
	"/bin/sh", \
	"-c", \
	"exec /usr/bin/pwnableserver --listen --no-chroot --alarm $TIMELIMIT --port $PORT --user $CHALLENGE_NAME --password \"$CHALLENGE_PASSWORD\" --exec /home/$CHALLENGE_NAME/wrapper.sh $PWNABLESERVER_EXTRA_ARGS" \
]
