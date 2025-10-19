#!/bin/bash

docker run --privileged multiarch/qemu-user-static --reset -p yes >/dev/null 2>&1

docker build --platform linux/arm64 -t daytona .

docker rm -f daytona
docker run --restart=always --read-only --name daytona -d -p 25606:25606 --platform linux/arm64 daytona
