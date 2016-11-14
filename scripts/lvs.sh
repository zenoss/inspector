#!/bin/bash
#
# zenoss-inspector-tags verify
#

lvs --all -o+lv_kernel_major,lv_kernel_minor,seg_monitor
