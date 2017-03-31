#!/bin/bash

# zenoss-inspector-tags verify serviced-delegate
# zenoss-inspector-deps systemctl-status.sh

SERVICED_RUNNING=false
grep --after-context=4 serviced systemctl-status.sh.stdout | grep ActiveState=active
if [ $? -eq 0 ]; then
    SERVICED_RUNNING=true
fi
echo "SERVICED_RUNNING=$SERVICED_RUNNING"
