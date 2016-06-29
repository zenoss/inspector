#!/bin/bash

# zenoss-inspector-info
# zenoss-inspector-tags os

command -v lsb_release >/dev/null 2>&1
if [ $? -ne 0 ]; then
   echo "lsb_release is not installed; distribution details not available."
   exit 0;
fi

lsb_release -a
