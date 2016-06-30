#!/bin/bash

# zenoss-inspector-tags slow os

command -v lsof >/dev/null 2>&1
if [ $? -ne 0 ]; then
   echo "lsof is not installed." 1>&2
   exit 1;
fi

lsof
