#!/bin/bash

cd src/server
docker build -t space-race .
docker rm -f space-race
docker run -d --restart=always --name space-race -p 25102:1337 space-race
