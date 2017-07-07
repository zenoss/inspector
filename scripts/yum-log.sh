#!/bin/bash

# zenoss-inspector-tags yum os

if [ -f /var/log/yum.log ]; then
	CURRENT_DIR=`pwd`
	pushd /var/log
	tar -cvf ${CURRENT_DIR}/yum-log.tar.gz -z yum*
	popd
fi
