#!/bin/bash

# zenoss-inspector-tags docker

echo "============================="
echo "output from 'docker version':"
echo "============================="
docker version

echo "============================="
echo "RPM information for docker"
echo "============================="
rpm -qa | grep docker
