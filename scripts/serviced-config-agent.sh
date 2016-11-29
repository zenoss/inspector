#!/bin/bash

# zenoss-inspector-info
# zenoss-inspector-tags config serviced serviced-worker verify
# zenoss-inspector-deps serviced-config.sh serviced-version.sh

# Verify that if this is a master node, that it is also an agent

grep -E -i 'SERVICED_MASTER=(1|true|t|yes)' serviced-config.sh.stdout &>/dev/null
if [ $? -ne 0 ]
then
    exit
fi

CC_VERSION=`grep -w 'Version:' serviced-version.sh.stdout 2>/dev/null | awk '{print $2}' | cut -d\. -f1-2`
if [[ "$CC_VERSION" == "1.0" || "$CC_VERSION" == "1.1" ]]
then
        grep -E -i "SERVICED_AGENT=(1|true|t|yes)" serviced-config.sh.stdout &>/dev/null
        if [ $? -ne 0 ]
        then
            echo "CHECK FAILED: SERVICED_AGENT must be enabled on the Master for serviced commands to work"
        fi
fi
