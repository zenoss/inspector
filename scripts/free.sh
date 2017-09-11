#!/bin/bash

# zenoss-inspector-tags os

free  -h -l -t

echo "Top memory usage:"
ps -eo pmem,pcpu,vsize,pid,cmd | sort -k 1 -nr | head -5

echo "Memory usage since midnight:"
sar -r
