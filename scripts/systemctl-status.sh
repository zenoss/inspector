#!/bin/bash

# zenoss-inspector-tags docker serviced serviced-worker verify

systemctl show --property=Names,Description,LoadState,ActiveState,UnitFileState dnsmasq
systemctl show --property=Names,Description,LoadState,ActiveState,UnitFileState docker
systemctl show --property=Names,Description,LoadState,ActiveState,UnitFileState firewalld
systemctl show --property=Names,Description,LoadState,ActiveState,UnitFileState ntpd
systemctl show --property=Names,Description,LoadState,ActiveState,UnitFileState serviced
