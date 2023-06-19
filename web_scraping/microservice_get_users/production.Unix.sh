#!/usr/bin/env bash
set -e

DOCKER_MICROSERVICE_GET_USERS="microservice_get_users"

DOCKER_VERSION_IMG="1.2.0-prod"

# build browser
docker build --no-cache --platform linux/amd64 -t $DOCKER_MICROSERVICE_GET_USERS .

# Push version
docker tag $DOCKER_MICROSERVICE_GET_USERS semillerosmart/microservice_get_users:$DOCKER_VERSION_IMG

docker push semillerosmart/microservice_get_users:$DOCKER_VERSION_IMG

# Push latest version
docker tag $DOCKER_MICROSERVICE_GET_USERS semillerosmart/microservice_get_users:latest
docker push semillerosmart/microservice_get_users:latest