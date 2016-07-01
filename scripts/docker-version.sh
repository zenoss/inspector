#!/bin/bash

# zenoss-inspector-tags rpm docker
# zenoss-inspector-deps get-rpms.sh

echo "============================="
echo "output from 'docker version':"
echo "============================="
docker version

echo "============================="
echo "RPM information for docker"
echo "============================="
grep docker get-rpms.sh.stdout
