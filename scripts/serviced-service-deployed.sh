#!/bin/bash

# zenoss-inspector-tags verify
# zenoss-inspector-deps serviced-service-list-v.sh

SERVICES_DEPLOYED=false
if [ -s serviced-service-list-v.sh.stdout ]; then
    SERVICES_DEPLOYED=true
fi
echo "SERVICES_DEPLOYED=$SERVICES_DEPLOYED"
