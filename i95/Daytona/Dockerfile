FROM alpine:3.18

RUN apk add --no-cache socat

RUN addgroup -S ctf && adduser -S -G ctf ctf
WORKDIR /home/ctf

COPY flag.txt ./flag.txt
COPY conn.sh ./conn.sh
COPY daytona ./daytona

EXPOSE 25606

CMD ["sh", "-c", "socat TCP-LISTEN:25606,reuseaddr,fork EXEC:./conn.sh,su=ctf,stderr,setsid,sigint"]
