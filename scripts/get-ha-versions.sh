#!/bin/bash

# zenoss-inspector-tags rpm ha verify
# zenoss-inspector-deps get-rpms.sh

HAS_DRBD=false
grep drbd get-rpms.sh.stdout
if [ $? -eq 0 ]; then
    HAS_DRBD=true
fi

HAS_PCS=false
egrep 'pcs|pacemaker|corosync' get-rpms.sh.stdout
if [ $? -eq 0 ]; then
    HAS_PCS=true
fi

grep serviced-resource-agents get-rpms.sh.stdout

echo "HAS_DRBD=$HAS_DRBD"
echo "HAS_PCS=$HAS_PCS"
