#!/bin/bash
#
# zenoss-inspector-tags serviced-delegate verify
#

lvs --all -o+lv_kernel_major,lv_kernel_minor,seg_monitor
