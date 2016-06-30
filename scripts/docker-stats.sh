#!/bin/bash

# zenoss-inspector-tags docker

docker ps -q | xargs docker stats --no-stream

