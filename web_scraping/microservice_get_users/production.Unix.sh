#!/usr/bin/env bash
set -e

DOCKER_MICROSERVICE_GET_USERS="microservice_get_users"

DOCKER_VERSION_IMG="1.0.0-prod"

# build browser
docker build -t $DOCKER_MICROSERVICE_GET_USERS .

# Push version
docker tag $DOCKER_MICROSERVICE_GET_USERS sebastiancb/microservice_get_users:$DOCKER_VERSION_IMG

docker push sebastiancb/microservice_get_users:$DOCKER_VERSION_IMG