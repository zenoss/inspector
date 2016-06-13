#!/bin/bash

# zenoss-inspector-info
# zenoss-inspector-tags serviced config
# zenoss-inspector-deps serviced-config.sh

# Verify that if this is a master node, that it is also an agent

grep "SERVICED_MASTER=1" serviced-config.sh.stdout &>/dev/null

if [ $? -eq 0 ]
    then
        grep "SERVICED_AGENT=1" serviced-config.sh.stdout &>/dev/null
        if [ $? -ne 0 ]
            then echo "CHECK FAILED: SERVICED_AGENT must be enabled on the Master for serviced commands to work"
        fi
fi
