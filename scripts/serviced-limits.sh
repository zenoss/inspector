#!/bin/bash

# zenoss-inspector-tags config serviced

# We have to ignore all of the other 'serviced <x>' commands being run by inspector
pid=$(ps waux | grep 'serviced [s]erver' | awk '{ print $2 }')

cat /proc/${pid}/limits
