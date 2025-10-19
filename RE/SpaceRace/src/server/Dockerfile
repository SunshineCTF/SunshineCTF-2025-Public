FROM golang:1.22-alpine AS build
WORKDIR /src

COPY main.go main.go

RUN if [ ! -f go.mod ]; then go mod init rover && go mod tidy; fi

RUN CGO_DISABLED=1 GOOS=linux go build -trimpath -ldflags="-s -w" -o /out/server ./main.go

FROM alpine:3.20
RUN apk add --no-cache socat ca-certificates && \
    adduser -D -u 10001 ctf
WORKDIR /app
COPY --from=build /out/server /app/server
RUN chmod +x /app/server
USER ctf
EXPOSE 1337

ENTRYPOINT ["socat","-T60","tcp-l:1337,reuseaddr,fork","exec:/app/server"]
