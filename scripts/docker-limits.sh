#!/bin/bash

# zenoss-inspector-tags config docker

cat /proc/$(pidof dockerd || pidof docker)/limits
