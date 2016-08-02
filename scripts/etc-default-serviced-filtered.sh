#!/bin/bash

# zenoss-inspector-tags serviced serviced-worker ha verify

#
# Filter the CC configuration to exclude comments and blank links.
# This saves a little effort for downstream scripts which are only
# interested in variables which are actually defined.
#
egrep -v '^#|^$' /etc/default/serviced | sort
