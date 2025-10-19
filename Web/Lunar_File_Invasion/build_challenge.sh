#!/bin/bash

# TODO: have the emulation flag too
docker compose -f docker-compose.yml build
docker compose -f docker-compose.yml up