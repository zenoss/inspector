#!/bin/bash

# zenoss-inspector-info
# zenoss-inspector-tags serviced verify

if [ $(serviced host list | grep -v master | sed -e '1d' | wc -l) -ne $(serviced service list | grep collectorredis  | awk 'BEGIN {FS = " "} ; {sum+=$3} END {print sum}') ] ; then echo "collectorredis count doesn't appear to match host count" ; else echo "collectorredis instances match host count" ;  fi
