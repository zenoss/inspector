#!/bin/bash

# zenoss-inspector-info
# zenoss-inspector-tags selinux
# zenoss-inspector-deps selinux-config.sh

SELINUX_CONFIG=`grep "^SELINUX=" selinux-config.sh.stdout 2>/dev/null`
if [ $? -eq 0 ]; then
    VALUE=`echo ${SELINUX_CONFIG} | cut -d\= -f2`
    if [ "${VALUE}" == "enforcing" ]; then
        echo "SELINUX setting '${VALUE}' is incorrect; should be 'disabled' or 'permissive'"
        exit 0
    fi
fi
