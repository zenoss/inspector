#!/bin/bash

# zenoss-inspector-tags ha
# zenoss-inspector-deps get-ha-versions.sh

grep "HAS_PCS=true" get-ha-versions.sh.stdout >/dev/null 2>&1
if [ $? -ne 0 ]; then
	echo "PCS is not installed."
	exit 0
fi

pcs constraint
pcs property
pcs resource defaults
pcs resource show --full
