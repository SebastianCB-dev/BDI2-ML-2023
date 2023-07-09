#!/usr/bin/env bash
set -e

DOCKER_MICROSERVICE_FOLLOW_NEW_PEOPLE="microservice_follow_new_people"

DOCKER_VERSION_IMG="1.2.0-prod"

# build browser
docker build --no-cache --platform linux/amd64 -t $DOCKER_MICROSERVICE_FOLLOW_NEW_PEOPLE .

# Push version
docker tag $DOCKER_MICROSERVICE_FOLLOW_NEW_PEOPLE semillerosmart/microservice_follow_new_people:$DOCKER_VERSION_IMG
docker push semillerosmart/microservice_follow_new_people:$DOCKER_VERSION_IMG

# Push latest version
docker tag $DOCKER_MICROSERVICE_FOLLOW_NEW_PEOPLE semillerosmart/microservice_follow_new_people:latest
docker push semillerosmart/microservice_follow_new_people:latest