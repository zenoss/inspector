#!/bin/bash

# zenoss-inspector-info
# zenoss-inspector-tags slow os

command -v lsof >/dev/null 2>&1
if [ $? -ne 0 ]; then
   echo "lsof is not installed."
   exit 0;
fi

lsof
