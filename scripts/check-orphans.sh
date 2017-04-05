#!/bin/bash

# zenoss-inspector-info
# zenoss-inspector-tags config serviced verify
# zenoss-inspector-deps serviced-config.sh get-orphans.sh

grep 'Orphaned devices were found' get-orphans.sh.stdout 2>&1 >/dev/null
if [ $? -eq 0 ]; then
    echo "WARNING: Orphaned devices were found. Use 'serviced-storage check --clean' to remove"
    echo "         Check get-orphans.sh.stdout for information on which orphan(s) were found."
    echo "         Check the Control Center Reference Guide for information on using serviced-storage."
fi
