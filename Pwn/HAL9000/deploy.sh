#!/bin/bash

docker build -t hal9000 .

docker rm -f hal9000 >/dev/null 2>&1
docker run --restart=always --name hal9000 -d -p 25005:25005 hal9000
