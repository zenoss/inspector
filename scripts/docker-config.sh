#!/bin/bash

# zenoss-inspector-tags docker verify

# CC/RM appliances have historically set some values directly in the systemd conf files
if [ -f /etc/systemd/system/docker.service.d/docker.conf ]; then
	cat /etc/systemd/system/docker.service.d/docker.conf
fi

# However, our documented procedures recommened customizations should be defined
# in a different location, so check there as well
if [ -f /etc/sysconfig/docker ]; then
	cat /etc/sysconfig/docker
fi
