#!/bin/bash

# zenoss-inspector-tags cpu os

# Get the results from nproc to show the number of cpus availahle to this process.
echo "Processors available: `nproc`"
echo

# Show CPU information.
lscpu
