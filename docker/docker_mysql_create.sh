#!/bin/bash
#set -x
# https://earthly.dev/blog/docker-mysql/

# Following doc from: https://hub.docker.com/_/mysql
CONTAINER_NAME=mysql_inova
PASS=mysql
FOLDER=$(dirname $(realpath -s $0))

echo ${FOLDER}
### Starting Container ###
docker run --name ${CONTAINER_NAME} -d -p 3306:3306 -v ${FOLDER}/data:/var/lib/mysql -e  MYSQL_ROOT_PASSWORD=${PASS} mysql:8 

#  see logs docker logs mysql --follow
