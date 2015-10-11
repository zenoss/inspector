#!/bin/bash

# zenoss-inspector-info
# zenoss-inspector-deps ps-aux.sh

grep "docker -d" ps-aux.sh.stdout &>/dev/null

if [ $? -ne 0 ]
    then
        grep "docker daemon" ps-aux.sh.stdout &>/dev/null
        if [ $? -ne 0 ]
            then echo "Docker doesn't appear to be running."
        fi
fi
