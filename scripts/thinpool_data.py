#!/usr/bin/env python
##############################################################################
#
# Copyright (C) Zenoss, Inc. 2017, all rights reserved.
#
# This content is made available according to terms specified in
# License.zenoss under the directory where your Zenoss product is installed.
#
##############################################################################
#
# Gathers the thinpool data used in other scripts.
#
##############################################################################

# zenoss-inspector-tags verify
# zenoss-inspector-deps serviced-config.sh

import lib.thinpool_stats as thinpool_stats
from pprint import pprint

if __name__ == "__main__":
    data = thinpool_stats.get_thinpool_data()
    pprint(data)