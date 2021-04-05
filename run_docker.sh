#!/usr/bin/env bash

# below uses the default value if $1 is not passed as an argument ... 

# set up the default image
DOCKER_IMAGE="${1:-pyfwa}"

docker run -v /Users/dt230133:/root -v /var/log:/apps/log ${DOCKER_IMAGE} --base_record 42 
