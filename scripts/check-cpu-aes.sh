#!/bin/bash

# zenoss-inspector-info
# zenoss-inspector-tags cpu os verify
# zenoss-inspector-deps cpuinfo.sh

cat cpuinfo.sh.stdout | grep -E "flags.*:.*aes" > /dev/null

if [ $? -ne 0 ]; then
    echo "The aes flag is missing from /proc/cpuinfo. Check virtualization compatibility flag."
fi

