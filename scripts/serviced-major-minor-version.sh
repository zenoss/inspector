#!/bin/bash

# zenoss-inspector-tags config serviced serviced-worker verify

serviced version | grep -w 'Version:' | awk '{print $2}' | cut -d\. -f1-2


