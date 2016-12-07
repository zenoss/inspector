#!/bin/bash

# zenoss-inspector-info
# zenoss-inspector-tags process docker
# zenoss-inspector-deps ps-aux.sh

egrep "(docker -d|docker daemon|dockerd)" ps-aux.sh.stdout &>/dev/null

if [ $? -ne 0 ]
    then echo "Docker doesn't appear to be running."
fi
