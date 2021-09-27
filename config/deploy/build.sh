#!/bin/bash

# if any of the commands in your code fails for any reason, the entire script fails
set -o errexit
# exits if any of your variables is not set
set -o nounset


echo "Starting to deploy docker image.."

SERVICE_NAME=cityapl_auth_service
DOCKER_CRED=cityapl@123
GIT_CRED=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

sudo rm -rf ${SERVICE_NAME}
git clone https://deepdik:${GIT_CRED}@github.com/deepdik/${SERVICE_NAME}.git

cd ${SERVICE_NAME}

sudo docker-compose stop
sudo docker image prune -a -f 
sudo docker login https://docker-registry.cityapl.com -u cityapl_docker_registry -p ${DOCKER_CRED}
sudo docker-compose pull
sudo docker-compose up -d

exit

###########################################################
