#!/bin/bash

# zenoss-inspector-tags os

command -v lsb_release >/dev/null 2>&1
if [ $? -ne 0 ]; then
   echo "lsb_release is not installed." 1>&2
   exit 1;
fi

lsb_release -a
