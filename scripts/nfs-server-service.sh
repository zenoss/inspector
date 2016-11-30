#!/bin/bash

# RM installation doc 1.2 recommends to use nfs-server drop-in conf files

CC_VERSION=`grep -w 'Version:' serviced-version.sh.stdout 2>/dev/null | awk '{print $2}' | cut -d\. -f1-2`

if [[ $CC_VERSION == "1.0" || $CC_VERSION == "1.1" ]]
then
    [[ -f /lib/systemd/system/nfs-server.service ]] && cat /lib/systemd/system/nfs-server.service
elif [[ $CC_VERSION == "1.2" ]]
then
    [[ -f /etc/systemd/system/nfs-server.service.d/nfs-server.conf ]] && cat /etc/systemd/system/nfs-server.service.d/nfs-server.conf
fi
