#!/bin/bash
#
# This script captures information about the OS storage configuration on the
# host machine.

echo "============================="
echo "output from 'lsblk':"
echo "============================="
lsblk

echo "============================="
echo "output from 'lvdisplay':"
echo "============================="
lvdisplay

echo "============================="
echo "output from 'vgdisplay':"
echo "============================="
vgdisplay

echo "============================="
echo "output from 'pvdisplay':"
echo "============================="
pvdisplay

echo "============================="
echo "output from 'dmsetup ls':"
echo "============================="
dmsetup ls --tree
