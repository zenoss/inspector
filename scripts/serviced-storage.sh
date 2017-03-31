#!/bin/bash

# zenoss-inspector-tags serviced verify

serviced-storage status -o=dm.thinpooldev=serviced-serviced--pool /opt/serviced/var/volumes
