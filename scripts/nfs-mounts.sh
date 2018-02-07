#!/bin/bash

# zenoss-inspector-deps serviced-major-minor-version.sh
# zenoss-inspector-tags config serviced serviced-delegate verify

# RM installation doc 1.2 recommends to use nfs-server drop-in conf files

[[ -f /etc/nfsmount.conf ]] && cat /etc/nfsmount.conf
