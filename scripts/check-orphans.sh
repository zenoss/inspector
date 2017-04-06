#!/bin/bash

# zenoss-inspector-info
# zenoss-inspector-tags config serviced verify
# zenoss-inspector-deps serviced-config.sh get-orphans.sh

grep 'Orphaned devices were found' get-orphans.sh.stdout 2>&1 >/dev/null
if [ $? -eq 0 ]; then
    THINPOOL_DEV_NAME=`grep SERVICED_DM_THINPOOLDEV= serviced-config.sh.stdout | awk -F'=' '{print $2}'`

    echo "WARNING: Orphaned devices were found. Use 'serviced-storage check --clean' to remove"
    echo "         e.g. 'serviced-storage check --clean -o=dm.thinpooldev=$THINPOOL_DEV_NAME /opt/serviced/var/volumes'"
    echo "         See get-orphans.sh.stdout for information on which orphan(s) were found."
    echo "         See the Control Center Reference Guide for information on using serviced-storage."
fi
