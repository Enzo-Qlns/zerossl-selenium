#/bin/bash

docker compose down
docker rmi --force zerossl-selenium-app:latest

docker compose up -d