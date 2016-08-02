#!/bin/bash

# zenoss-inspector-tags ha verify
# zenoss-inspector-deps get-ha-versions.sh get-ha-config.sh etc-default-serviced-filtered.sh

function verify_vip() {
	result=0
	VIP_VALUE=$1
	configVar=$2
	required=$3

	configValue=`grep $configVar etc-default-serviced-filtered.sh.stdout 2>/dev/null`
	if [[ -z "$configValue" ]]; then
		if [ "$required" == "true" ]; then
			echo "ControlCenter configuration variable $configVar is not defined"
			result=1
		fi
		return $result
	fi

	configIP=`echo "$configValue" | cut -d\= -f2  | cut -d: -f1`
	if [ "$configIP" != "$VIP_VALUE" ]; then
		echo "ControlCenter configuration variable $configVar does not contain the HA Virtual IP: $VIP_VALUE"
		result=1
	fi
	return $result
}

grep "HAS_PCS=true" get-ha-versions.sh.stdout >/dev/null 2>&1
if [ $? -ne 0 ]; then
	echo "PCS is not installed."
	exit 0
fi

RC=0

# Check the Ordering contstraint. The DFSMaster resource should be started first,
#   followed by the resource group 'serviced-group'
grep 'promote DFSMaster then start serviced-group' get-ha-config.sh.stdout >/dev/null 2>&1
if [ $? -ne 0 ]; then
	echo "Check Ordering Constraints; should be 'promote DFSMaster then start serviced-group'"
	RC=1
fi

# Check the Colocation contstraint. The resource group 'serviced-group' should always
#    be started on the same node as the DFSMaster resource
grep 'serviced-group with DFSMaster' get-ha-config.sh.stdout >/dev/null 2>&1
if [ $? -ne 0 ]; then
	echo "Check Colocation Constraints; should be 'serviced-group with DFSMaster'"
	RC=1
fi

# Check resource-stickiness. A stickiness value of 100 keeps all resources on the same node.
grep 'resource-stickiness: 100' get-ha-config.sh.stdout >/dev/null 2>&1
if [ $? -ne 0 ]; then
	echo "Check resource defaults; missing the default 'resource-stickiness: 100'"
	RC=1
fi

# Check the quorum policy. For 2-node configurations, no quorum is required.
grep 'no-quorum-policy: ignore' get-ha-config.sh.stdout >/dev/null 2>&1
if [ $? -ne 0 ]; then
	echo "Check resource defaults; missing the default 'no-quorum-policy: ignore'"
	RC=1
fi

#
# Get the value of the floating virtual IP.
VIP_VALUE=`grep ip= get-ha-config.sh.stdout  | awk '{print $2}' | cut -d\= -f 2`

#
# The list of CC master vars that SHOULD contain the cluster's Virtual IP, if they
# are defined.
VIP_OPTIONAL_VARS="SERVICED_LOG_ADDRESS
SERVICED_LOGSTASH_ES
SERVICED_STATS_PORT"
for configVar in `echo $VIP_OPTIONAL_VARS`
do
	verify_vip $VIP_VALUE $configVar false
	if [ $? -ne 0 ]; then
		RC=1
	fi
done

#
# The list of CC master vars that MUST be defined with the cluster's Virtual IP
VIP_REQUIRED_VARS="SERVICED_DOCKER_REGISTRY SERVICED_ENDPOINT
SERVICED_OUTBOUND_IP
SERVICED_ZK"
for configVar in `echo $VIP_REQUIRED_VARS`
do
	verify_vip $VIP_VALUE $configVar false
	if [ $? -ne 0 ]; then
		RC=1
	fi
done

# WIP - check NFS interval
NFS_INTERVAL_CONFIG=`grep nfs-monitor-interval get-ha-config.sh.stdout`
if [ $? -ne 0 ]; then
	echo "ERROR: did find nfs-monitor-interval in HA config"
	RC=1
else
	NFS_INTERVAL=`echo $NFS_INTERVAL_CONFIG | awk '{print $3}' | cut -d\= -f 2`
	if [[ "$NFS_INTERVAL" != "0" && "$NFS_INTERVAL" != "0s" ]]; then
		echo "ERROR: HA nfs-monitor-interval should be 0; not $NFS_INTERVAL"
		RC=1
	fi
fi


exit $RC
