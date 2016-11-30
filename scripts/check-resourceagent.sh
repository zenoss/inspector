#!/bin/bash

# zenoss-inspector-info
# zenoss-inspector-tags rpm docker ha verify os
# zenoss-inspector-deps get-ha-versions.sh get-rpms.sh

grep "HAS_PCS=true" get-ha-versions.sh.stdout >/dev/null 2>&1
if [ $? -ne 0 ]; then
	exit 0
fi

MIN_VERSION="0.0.9"

RESOURCE_VERSION=`grep serviced-resource-agents get-rpms.sh.stdout 2>/dev/null  | cut -d\- -f4  2>/dev/null`
if [ -z "${RESOURCE_VERSION}" ]
then
	echo "ERROR: can not determine version for the RPM named serviced-resource-agents"
	exit 1
fi

if [[ "${RESOURCE_VERSION}" < "${MIN_VERSION}" ]]
then
	echo "Version ${RESOURCE_VERSION} of the RPM serviced-resource-agents is too old."
	echo "The recommended version is ${MIN_VERSION} or higher"
fi
