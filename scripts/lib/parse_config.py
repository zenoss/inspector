#!/bin/python
##############################################################################
#
# Copyright (C) Zenoss, Inc. 2017, all rights reserved.
#
# This content is made available according to terms specified in
# License.zenoss under the directory where your Zenoss product is installed.
#
##############################################################################
#
# Parses the contents of the serviced-config.sh script into a dictionary.
#
##############################################################################

def parse_serviced_config():
    '''
    Parse the serviced-config output into a dict for later use.
    '''
    with open('serviced-config.sh.stdout', 'r') as f:
        lines = f.readlines()

    config = {}
    for line in lines:
        line = line.strip()
        if "=" in line and not line.strip().startswith("#"):
            data = line.split("=", 1)
            config[data[0].strip()] = data[1].strip()
    return config
