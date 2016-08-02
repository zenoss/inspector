#!/bin/bash

# zenoss-inspector-tags ha
# zenoss-inspector-deps get-ha-versions.sh

grep "HAS_PCS=true" get-ha-versions.sh.stdout >/dev/null 2>&1
if [ $? -ne 0 ]; then
	echo "PCS is not installed."
	exit 0
fi

#
# The OCF log function writes messages in the format:
#    resourceAgent(resourceName)[PID]: level: message
# For example,
#    LVM(serviced-lvm)[2015]: INFO: Deactivating volume group serviced
#
grep '.*(.*)\[.*\]:' /var/log/messages
if [ $? -ne 0 ]; then
	echo "No log messages found for any OCF resource agent" 1>&2
	exit 1
fi
