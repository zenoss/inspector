#!/bin/bash

# zenoss-inspector-tags docker
# zenoss-inspector-deps ps-aux.sh

egrep "(docker -d|docker daemon|dockerd)" ps-aux.sh.stdout &>/dev/null

if [ $? -ne 0 ]; then
    (>&2 echo "Docker doesn't appear to be running.")
    exit 1
fi

docker ps -q | xargs docker stats --no-stream

