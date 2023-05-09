#!/usr/bin/env bash
set -e

DOCKER_MICROSERVICE_GET_COMMENTS="microservice_get_comments"

DOCKER_VERSION_IMG="1.0.0-prod"

# build browser
docker build --no-cache -t $DOCKER_MICROSERVICE_GET_COMMENTS .

# Push version
docker tag $DOCKER_MICROSERVICE_GET_COMMENTS semillerosmart/microservice_get_comments:$DOCKER_VERSION_IMG

docker push semillerosmart/microservice_get_comments:$DOCKER_VERSION_IMG