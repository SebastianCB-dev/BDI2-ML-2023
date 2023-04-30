#!/usr/bin/env bash
set -e

DOCKER_MICROSERVICE_GET_COMMENTS="microservice_get_comments"

DOCKER_VERSION_IMG="1.0.1-prod"

# build browser
docker build -t $DOCKER_MICROSERVICE_GET_COMMENTS .

# Push version
docker tag $DOCKER_MICROSERVICE_GET_COMMETS sebastiancb/microservice_get_comments:$DOCKER_VERSION_IMG

docker push sebastiancb/microservice_get_comments:$DOCKER_VERSION_IMG