FROM mcr.microsoft.com/powershell:alpine-3.17

RUN apk add --update socat

# note: this Dockerfile is based on https://github.com/SunshineCTF/SunshineCTF-2017-Public/blob/master/Pwn/400-Notetorious/Dockerfile

# Create unprivileged unprivileged user. lol.
RUN addgroup -S unprivileged && \
	adduser -S unprivileged -G unprivileged && \
    mkdir /app

# start out of app, install to app.
WORKDIR /app
COPY ./flag.txt ./server/evil_corp_ai.ps1 ./server/access_token.txt /app/

# make sure the files are owned by root but visible by the unprivileged group
RUN chown root:root /app /app/flag.txt /app/access_token.txt /app/evil_corp_ai.ps1 && \
	chmod 0555 /app /app/evil_corp_ai.ps1 && \
	chmod 0444 /app/flag.txt

# listens on the following port.
EXPOSE 25006/tcp
CMD socat -T 600 TCP-LISTEN:25006,fork,reuseaddr EXEC:"/usr/bin/pwsh /app/evil_corp_ai.ps1",su=unprivileged,pty,ctty,echo=0,stderr
