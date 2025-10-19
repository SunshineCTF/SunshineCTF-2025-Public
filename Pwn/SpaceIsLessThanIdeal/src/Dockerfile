FROM alpine:3.22 AS build
RUN apk add --update \
    gcc \
    libc-dev

WORKDIR /build
COPY ./setuid-cat.c /build
COPY ./drop-groups.c /build
RUN gcc setuid-cat.c -o cat-flag
RUN gcc drop-groups.c -o drop-perms

FROM alpine:3.22
RUN apk add --update \
    socat \
    newt \
    libcap-utils \
    less

# note: this Dockerfile is based on https://github.com/SunshineCTF/SunshineCTF-2017-Public/blob/master/Pwn/400-Notetorious/Dockerfile

# Create unprivileged unprivileged user. lol.
RUN addgroup -S unprivileged && \
	adduser -S unprivileged -G unprivileged -s /bin/nologin && \
    addgroup -S flag-read

# start out of app, install to app.
WORKDIR /app
COPY ./challenge.sh ./fake-term.sh ./flag.txt ./system_logs.txt /app/
COPY --from=build /build/cat-flag /app/cat-flag
COPY --from=build /build/drop-perms /app/drop-perms

# make sure the files are owned by root but visible by the unprivileged group
RUN chown -R root:root /app && \
	chmod 0440 /app/* && \
	chmod 0555 /app /app/challenge.sh /app/fake-term.sh /app/cat-flag /app/drop-perms && \
    chmod 0444 /app/system_logs.txt && \
    chown root:flag-read /app/flag.txt /app/cat-flag && \
    setcap cap_setgid+ep /app/drop-perms && \
    chmod g+s /app/cat-flag

# listens on the following port.
EXPOSE 25003/tcp
# this year because the TTY was actually needed, had to do setgid/setuid early instead of su, but also had to drop supplementary groups
CMD socat -T 600 TCP-LISTEN:25003,fork,reuseaddr EXEC:"/app/drop-perms",setgid-early=unprivileged,setuid-early=unprivileged,pty,ctty,echo=0,sane,stderr
