#/bin/bash

docker compose down
docker rmi --force zerossl-selenium-app:latest selenium/standalone-chrome:latest

docker compose up -d