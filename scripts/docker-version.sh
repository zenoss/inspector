#!/bin/bash

echo "============================="
echo "output from 'docker version':"
echo "============================="
docker version

echo "============================="
echo "RPM information for docker"
echo "============================="
rpm -qa | grep docker
