#!/bin/bash

# zenoss-inspector-deps serviced-major-minor-version.sh
# zenoss-inspector-tags config serviced serviced-delegate verify

# RM installation doc 1.2 recommends to use nfs-server drop-in conf files

CC_VERSION=$(cat serviced-major-minor-version.sh.stdout)

if [[ $CC_VERSION == "1.0" || $CC_VERSION == "1.1" ]]
then
    [[ -f /lib/systemd/system/nfs-server.service ]] && cat /lib/systemd/system/nfs-server.service
else
    [[ -f /etc/systemd/system/nfs-server.service.d/nfs-server.conf ]] && cat /etc/systemd/system/nfs-server.service.d/nfs-server.conf
fi
