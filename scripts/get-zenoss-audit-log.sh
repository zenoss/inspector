#!/bin/bash
# zenoss-inspector-tags auditlogs
# Resource Manager audit log

if [ -f /var/log/serviced/application-audit.log ]; then
	sudo cat /var/log/serviced/application-audit.log
else
	echo "Zenoss audit log doesn't exist" 1>&2
	exit 1
fi
