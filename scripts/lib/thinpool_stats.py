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
# Returns stats on the serviced data and metadata volumes.  This doesn't try
# to mount the tenant volumes to get stats on those.
#
##############################################################################

import re
import subprocess

import sizefmt
import parse_config


def get_serviced_settings(config):
    """
    Returns the min data and metadata storage sizes. CC interprets SERVICED_STORAGE_MIN_FREE
    with base 1024, so we need to coerce the value when we parse it.
    """
    data = {}
    s_storage_min_free = config.get("SERVICED_STORAGE_MIN_FREE", "3G")
    data['SERVICED_STORAGE_MIN_FREE'] = s_storage_min_free
    s_storage_min_free = s_storage_min_free.lower() # coerce to base 1024 to match CC interpretation.
    storage_min_free = sizefmt.parse_size(s_storage_min_free) or (3 * sizefmt.GiB) # Default setting if we can't parse.
    data['data_min_free'] = storage_min_free
    data['meta_min_free'] = int(storage_min_free * 0.02)
    return data


def calc_tpool_stats(stats):
    """
    Calculates the thinpool stats based on the lvs output provided and returns them.

    >>> calc_tpool_stats('  100.00g 1.00   1.00g 2.00')['data_size']
    107374182400.0
    >>> calc_tpool_stats('  100.00g 1.00   1.00g 2.00')['data_percent']
    0.01
    >>> calc_tpool_stats('  100.00g 1.00   1.00g 2.00')['meta_size']
    1073741824.0
    >>> calc_tpool_stats('  100.00g 1.00   1.00g 2.00')['meta_percent']
    0.02
    >>> calc_tpool_stats('  100.00g 1.00   1.00g 2.00')['meta_free']
    1052266987.52
    >>> calc_tpool_stats('  100.00g 1.00   1.00g 2.00')['meta_used']
    21474836.48
    >>> calc_tpool_stats('  100.00g 1.00   1.00g 2.00')['data_free']
    106300440576.0
    >>> calc_tpool_stats('  100.00g 1.00   1.00g 2.00')['data_used']
    1073741824.0
    """
    data = {}
    stats = filter(None, stats.split(' '))
    data['data_size'] = sizefmt.parse_size(stats[0])
    data['data_percent'] = sizefmt.parse_size(stats[1]) / 100
    data['data_used'] = data['data_size'] * data['data_percent']
    data['data_free'] = data['data_size'] * (1-data['data_percent'])
    data['meta_size'] = sizefmt.parse_size(stats[2])
    data['meta_percent'] = sizefmt.parse_size(stats[3]) / 100
    data['meta_used'] = data['meta_size'] * data['meta_percent']
    data['meta_free'] = data['meta_size'] * (1-data['meta_percent'])
    return data


def get_tpool_stats(config):
    """
    Returns a mapping representing data for the serviced thinpool.
    """
    thinpooldev = config.get("SERVICED_DM_THINPOOLDEV", "serviced")
    cmd = "lvs -o lv_size,data_percent,lv_metadata_size,metadata_percent %s 2>/dev/null | grep -vi lsize" % thinpooldev
    stats = subprocess.check_output(cmd, shell=True).strip()
    if not stats:
        return {}
    data = calc_tpool_stats(stats)
    data['thinpooldev'] = thinpooldev
    return data


def get_tenant_stats():
    """
    Uses df to get free space for mounted tenant volumes (if any). df -h shows
    base 1024 stats, so we need to parse these appropriately.
    """
    data = { 'tenants': [] }
    cmd = "df -h --output=avail,target | grep /opt/serviced/var/volumes 2>/dev/null || true"
    stats = subprocess.check_output(cmd, shell=True)
    if not stats:
        return data
    for line in [s.strip() for s in stats.split('\n') if s != '']:
        line = line.split(' ')
        if len(line) != 2: continue
        tenant = line[1].split('/')[-1]
        free = sizefmt.parse_size(line[0].lower())
        data['tenants'].append({ 'id': tenant, 'free': free })
    return data


def get_thinpool_data():
    """
    Returns a map of data for the serviced thin pool.
    """
    config = parse_config.parse_serviced_config()
    data = get_serviced_settings(config)
    data.update(get_tpool_stats(config))
    data.update(get_tenant_stats())
    return data


if __name__ == '__main__':
     # If run, make sure test cases pass.
     import doctest
     doctest.testmod()
