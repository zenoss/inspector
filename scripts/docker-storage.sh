#!/bin/bash

# zenoss-inspector-info
# zenoss-inspector-tags docker
# zenoss-inspector-deps docker-info.sh

# First make sure docker is using devicemapper
# Note that if we skip all checks don't have docker-info.sh.stdout
# (e.g. docker wasn't running)
DRIVER_CONFIG=`grep "Storage Driver:" docker-info.sh.stdout 2>/dev/null`
if [ $? -eq 0 ]; then
    DRIVER=`echo ${DRIVER_CONFIG} | awk '{print $3}' `
    if [ "${DRIVER}" != "devicemapper" ]; then
        echo "Docker Storage Driver '${DRIVER}' is incorrect; should be 'devicemapper'"
        exit 0
    fi

    # If docker is using devicemapper, make sure it is not backed by a
    # loopback device which can be an order of magnitude slower than a thinpool
    grep "Data file: /dev/loop" docker-info.sh.stdout &>/dev/null
    if [ $? -eq 0 ]; then
        echo "Docker is using a loopback device; use an LVM thinpool instead."
    fi
fi
