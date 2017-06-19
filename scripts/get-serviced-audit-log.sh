#!/bin/bash
# zenoss-inspector-tags auditlogs

# Control Center audit log

if [[ -f /var/log/serviced/serviced-audit.log ]]; then
	sudo cat /var/log/serviced/serviced-audit.log
else
	echo "serviced audit log doesn't exist" 1>&2
	exit 1
fi
