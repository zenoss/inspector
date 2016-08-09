#!/bin/bash

# zenoss-inspector-tags slow os
# zenoss-inspector-deps get-rpms.sh

grep -w lsof get-rpms.sh.stdout
if [ $? -ne 0 ]; then
	echo "lsof is not installed."
	exit 0
fi

lsof
