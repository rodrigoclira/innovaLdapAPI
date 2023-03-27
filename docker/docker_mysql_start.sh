#!/bin/bash
#set -x
# https://earthly.dev/blog/docker-mysql/

# Following doc from: https://hub.docker.com/_/mysql
CONTAINER_NAME=mysql_inova

### Starting Container ###
docker start -a ${CONTAINER_NAME}  

#  see logs docker logs mysql --follow
