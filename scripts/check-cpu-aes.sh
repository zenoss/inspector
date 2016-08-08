#!/bin/bash

# zenoss-inspector-info
# zenoss-inspector-tags cpu os

cat /proc/cpuinfo | grep -E "flags.*:.*aes"

if [ $? -ne 0 ]; then
    echo "The aes flag is missing from /proc/cpuinfo. Check virtualization compatibility flag."
fi

