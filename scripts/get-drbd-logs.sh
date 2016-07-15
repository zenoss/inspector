#!/bin/bash

# zenoss-inspector-tags ha
# zenoss-inspector-deps get-ha-versions.sh get-kernel-logs.sh

grep "HAS_DRBD=true" get-ha-versions.sh.stdout >/dev/null 2>&1
if [ $? -ne 0 ]; then
	echo "DRBD is not installed."
	exit 0
fi

grep drbd get-kernel-logs.sh.stdout
