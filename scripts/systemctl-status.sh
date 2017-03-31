#!/bin/bash

# zenoss-inspector-tags docker serviced serviced-delegate verify ha
# zenoss-inspector-deps get-ha-versions.sh

systemctl show --property=Names,Description,LoadState,ActiveState,UnitFileState dnsmasq
systemctl show --property=Names,Description,LoadState,ActiveState,UnitFileState docker
systemctl show --property=Names,Description,LoadState,ActiveState,UnitFileState firewalld
systemctl show --property=Names,Description,LoadState,ActiveState,UnitFileState ntpd
systemctl show --property=Names,Description,LoadState,ActiveState,UnitFileState serviced

grep "HAS_PCS=true" get-ha-versions.sh.stdout >/dev/null 2>&1
if [ $? -eq 0 ]; then
	systemctl show --property=Names,Description,LoadState,ActiveState,UnitFileState corosync
	systemctl show --property=Names,Description,LoadState,ActiveState,UnitFileState pacemaker
fi
