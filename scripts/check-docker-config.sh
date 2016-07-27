#!/bin/bash

# zenoss-inspector-info
# zenoss-inspector-tags docker config verify
# zenoss-inspector-deps docker-config.sh

grep -i -- '--exec-opt native.cgroupdriver=cgroupfs' docker-config.sh.stdout &>/dev/null

if [ $? -ne 0 ]
    then
        echo "Incorrect docker config: Add '--exec-opt native.cgroupdriver=cgroupfs' to /etc/sysconfig/docker"
fi

grep -i -- '--storage-opt dm.thinpooldev=/dev/mapper/docker-docker--pool' docker-config.sh.stdout &>/dev/null

if [ $? -ne 0 ]
    then
        echo "Incorrect docker config: Add '--storage-opt dm.thinpooldev=/dev/mapper/docker-docker--pool' to /etc/sysconfig/docker"
fi
