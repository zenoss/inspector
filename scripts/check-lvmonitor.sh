#!/bin/bash
#
# zenoss-inspector-info
# zenoss-inspector-tags verify
# zenoss-inspector-deps lvs.sh

grep -w serviced-pool lvs.sh.stdout | grep 'not monitored' >/dev/null 2>&1
if [ $? -ne 0 ]; then
	echo "ERROR: serviced-pool is monitored by dmeventd"
	echo "       If this an HA system, upgrade to the latest verison of serviced-resource-agents"
	echo "       If this is not an HA system, use 'lvchange --monitor n serviced/serviced-pool' to disable monitoring"
fi

