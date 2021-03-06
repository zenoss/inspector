#!/bin/bash

# zenoss-inspector-tags config serviced verify
# zenoss-inspector-deps serviced-config.sh

# Verify that if this is a master node, that it is also an agent

grep -E -i 'SERVICED_MASTER=(1|true|t|yes)' serviced-config.sh.stdout &>/dev/null
if [ $? -ne 0 ]
then
    # Skip this check on delegate nodes
    echo "No storage check performed on this node because it is not a CC master."
    exit 0
fi

serviced-storage check --help 2>&1 | grep -i 'orphaned' 2>&1 >/devnull
if [ $? -ne 0 ]
then
    # Skip this check if serviced-storage too old to support 'check orphan'
    echo "No storage check performed on this node because 'serviced-storage check'"
    echo "is not supported on this version of Control Center."
    exit 0
fi

THINPOOL_DEV_NAME=`grep SERVICED_DM_THINPOOLDEV= serviced-config.sh.stdout | awk -F'=' '{print $2}'`
if [ -z "$THINPOOL_DEV_NAME" ]
then
    echo "ERROR: could find SERVICED_DM_THINPOOLDEV in serviced-config.sh.stdout"
    exit 1
fi

serviced-storage -v -v check -o=dm.thinpooldev=$THINPOOL_DEV_NAME /opt/serviced/var/volumes
