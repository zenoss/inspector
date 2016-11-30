#!/bin/bash

# RM installation doc recommends to use nfs-server drop-in conf files
if [ -f /etc/systemd/system/nfs-server.service.d/nfs-server.conf ]; then
    cat /etc/systemd/system/nfs-server.service.d/nfs-server.conf
fi
