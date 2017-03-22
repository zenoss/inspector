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
# Checks the serviced thinpool data and metadata to see if an upgrade would put the
# system into Emergency Shutdown mode.
#
# Some helper scripts that are broken out in the upgrade are included here
# to keep inspector from trying to run them as inspector scripts.
#
##############################################################################

# zenoss-inspector-info
# zenoss-inspector-tags verify
# zenoss-inspector-deps thinpool_data.py

import ast
import lib.sizefmt as sizefmt

def get_thinpool_data():
    '''
    Parses the output of the thinpool_data.py script into a dictionary.
    '''
    with open('thinpool_data.py.stdout', 'r') as f:
        lines = f.read()
    return ast.literal_eval(lines)


def check_thinpool():
    '''
    Returns "" if there are no problems, otherwise returns a string explaining
    what was too small.
    '''
    stats = get_thinpool_data()
    err = ""
    if stats['data_free'] < stats['data_min_free']:
        err += "\nThe thinpool storage free (%s) is under the minimum threshold (%s)" % \
            (sizefmt.humansize(stats['data_free']), sizefmt.humansize(stats['data_min_free']))
    if stats['meta_free'] < stats['meta_min_free']:
        err += "\nThe thinpool metadata free (%s) is under the minimum threshold (%s)" % \
            (sizefmt.humansize(stats['meta_free']), sizefmt.humansize(stats['meta_min_free']))
    return err


if __name__ == "__main__":
    err = check_thinpool()
    if err:
        print err
