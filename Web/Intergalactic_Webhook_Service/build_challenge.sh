#!/bin/bash

# build the docker image
docker build -t webhook-service ./src/

# run the image and expose port 5000
docker run -p 5000:5000 webhook-service