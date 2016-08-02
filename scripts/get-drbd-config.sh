#!/bin/bash

# zenoss-inspector-tags ha verify
# zenoss-inspector-deps get-ha-versions.sh

grep "HAS_DRBD=true" get-ha-versions.sh.stdout >/dev/null 2>&1
if [ $? -ne 0 ]; then
	echo "DRBD is not installed."
	exit 0
fi

if [ ! -f /etc/drbd.d/serviced-dfs.res ]; then
	echo "ERROR: /etc/drbd.d/serviced-dfs.res does not exist" 1>&2
	exit 1
fi

cat /etc/drbd.d/serviced-dfs.res
