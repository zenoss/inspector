#!/bin/bash

# zenoss-inspector-tags os
# zenoss-inspector-deps get-rpms.sh

grep -w lsb get-rpms.sh.stdout
if [ $? -ne 0 ]; then
	echo "lsb_release is not installed."
	exit 0;
fi

lsb_release -a
