#!/bin/bash

# zenoss-inspector-info
# zenoss-inspector-tags os

if [ ! -d "/var/log/journal" ]; then
  echo "/var/log/journal does not exist. Persistent storage for log files not enabled."
fi
