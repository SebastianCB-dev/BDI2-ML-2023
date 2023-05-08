#!/usr/bin/env bash
set -e

DOCKER_MICROSERVICE_GET_POSTS="microservice_get_posts"

DOCKER_VERSION_IMG="1.0.0-prod"

# build browser
docker build --no-cache -t $DOCKER_MICROSERVICE_GET_POSTS .

# Push version
docker tag $DOCKER_MICROSERVICE_GET_POSTS semillerosmart/microservice_get_posts:$DOCKER_VERSION_IMG

docker push semillerosmart/microservice_get_posts:$DOCKER_VERSION_IMG