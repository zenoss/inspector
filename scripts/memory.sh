#!/bin/bash

# zenoss-inspector-tags os

printf "\nOutput of the 'free' command:\n"
free  -h -l -t

printf "\nTop memory usage:\n"
ps -eo pmem,pcpu,vsize,pid,cmd | sort -k 1 -nr | head -5

printf "\nMemory usage since midnight:\n"
sar -r
