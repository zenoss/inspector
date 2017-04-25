#!/bin/bash
#
# zenoss-inspector-tags time-drift verify


HOST_IP=`hostname -i`
for i in $(serviced host list --show-fields Addr | grep -v ^Addr  | grep -v $HOST_IP); do
   echo ntpdate \-q $i
   ntpdate -q $i
done
exit 0
