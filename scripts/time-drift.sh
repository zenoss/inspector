#!/bin/bash
#
# zenoss-inspector-tags verify
#

for i in $(serviced host list| awk '{print $4}' | grep -v Name | grep -v $HOSTNAME); do echo ntpdate \-q $i; ntpdate -q $i; done
