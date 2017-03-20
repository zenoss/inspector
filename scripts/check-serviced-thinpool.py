#!/usr/bin/env python
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
# zenoss-inspector-deps serviced-config.sh

import re
import subprocess
import sys

##############################################################################
# size format helper functions

KB  = 1000
MB  = 1000 * KB
GB  = 1000 * MB
TB  = 1000 * GB
PB  = 1000 * TB

KiB = 1024
MiB = 1024 * KiB
GiB = 1024 * MiB
TiB = 1024 * GiB
PiB = 1024 * TiB

SIZES = {
    'b': 1, 'kb': KiB, 'mb': MiB, 'gb': GiB, 'tb': TiB, 'pb': PiB,
    'B': 1, 'Kb': KB, 'Mb': MB, 'Gb': GB, 'Tb': TB, 'Pb': PB,
}
decimapAbbrs = ['B', 'KB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB', 'YB']
binaryAbbrs = ['B', 'KiB', 'MiB', 'GiB', 'TiB', 'PiB', 'EiB', 'ZiB', 'YiB']
sizeRegex = re.compile("^([-]?)(\d+(.\d+)?) ?([KkMmGgTtPp])?(i)?([Bb])?$")

def parse_size(size):
    """
    Parses the human-readable size string into the amount it represents
    as a float value. Upper case units are base 1000, lowercase base 1024.
    If the unit has "i" in the middle it uses base 1024.

    >>> parse_size("10K")
    10000.0
    >>> parse_size("-10K")
    -10000.0
    >>> parse_size("10 KB")
    10000.0
    >>> parse_size("10 G")
    10000000000.0
    >>> parse_size("10GB")
    10000000000.0
    >>> parse_size("10k")
    10240.0
    >>> parse_size("-10k")
    -10240.0
    >>> parse_size("10 kb")
    10240.0
    >>> parse_size("10gb")
    10737418240.0
    >>> parse_size("10g")
    10737418240.0
    >>> parse_size("10GiB")
    10737418240.0
    """
    match = sizeRegex.match(size)
    if not match:
        return None
    neg = -1 if match.group(1) else 1
    m1 = float(match.group(2))
    m2 = match.group(4) if match.group(4) else ''
    if match.group(5): m2 = m2.lower()
    m3 = match.group(6).lower() if match.group(6) else 'b'
    return neg * m1 * SIZES[(m2 + m3)]


def customsize(size, base, map):
    neg = 1 if size >= 0 else -1
    size = size * neg
    i = 0
    while size >= base and i < len(map)-1:
        size = size / base
        i = i + 1
    size = str(round(size, 3) * neg).strip('0').strip('.') or "0"
    return '%s %s' % (size, map[i])


def humansize(size):
    """
    Converts the size string given into a human readable format
    using 1000 as the base.

    >>> humansize(0)
    '0 B'
    >>> humansize(-0)
    '0 B'
    >>> humansize(1234)
    '1.234 KB'
    >>> humansize(123456)
    '123.456 KB'
    >>> humansize(1234567890)
    '1.235 GB'
    >>> humansize(-1234567890)
    '-1.235 GB'
    """
    if not isinstance(size, (int, float)):
        raise ValueError('humansize() only takes int or float arguments')
    return customsize(size, 1000.0, decimapAbbrs)


def bytesize(size):
    """
    Converts the size string given into a human readable format
    using 1024 as the base.

    >>> bytesize(0)
    '0 B'
    >>> bytesize(-0)
    '0 B'
    >>> bytesize(1234)
    '1.205 KiB'
    >>> bytesize(123456)
    '120.563 KiB'
    >>> bytesize(1234567890)
    '1.15 GiB'
    >>> bytesize(-1234567890)
    '-1.15 GiB'
    >>> bytesize(1024*1024*1024)
    '1 GiB'
    """
    if not isinstance(size, (int, float)):
        raise ValueError('bytesize() only takes int or float arguments')
    return customsize(size, 1024.0, binaryAbbrs)


##############################################################################
# Gather serviced and thinpool data from the that we want. 

# Returns the min data and metadata storage sizes.
def get_serviced_settings(config):
    data = {}
    s_storage_min_free = config.get("SERVICED_STORAGE_MIN_FREE", "3G")
    storage_min_free = parse_size(s_storage_min_free) or (3 * GB) # Default setting if we can't parse.
    data['SERVICED_STORAGE_MIN_FREE'] = s_storage_min_free
    data['data_min_free'] = storage_min_free
    data['meta_min_free'] = int(storage_min_free * 0.02)
    return data


# Returns a mapping representing data for the serviced thinpool.
def get_tpool_stats(config):
    data = {}
    thinpooldev = config.get("SERVICED_DM_THINPOOLDEV", "serviced")
    cmd = "lvs -o lv_size,data_percent,lv_metadata_size,metadata_percent %s 2>/dev/null | grep -vi lsize" % thinpooldev
    stats = subprocess.check_output(cmd, shell=True).strip()
    if not stats:
        return data
    stats = filter(None, stats.split(' '))
    data['thinpooldev'] = thinpooldev
    data['data_size'] = parse_size(stats[0])
    data['data_percent'] = parse_size(stats[1])
    data['data_free'] = data['data_size'] * data['data_percent']
    data['meta_size'] = parse_size(stats[2])
    data['meta_percent'] = parse_size(stats[3])
    data['meta_free'] = data['meta_size'] * data['meta_percent']
    return data


# Parse the serviced-config output into a dict for later use.
def parse_serviced_config():
    with open('serviced-config.sh.stdout', 'r') as f:
        lines = f.readlines()

    data = {}
    for line in lines:
        line = line.strip()
        if line.startswith('#'):
            continue

        split = line.split("=")
        data[split[0].strip()] = split[1].strip()
    return data


# Returns a map of data for the serviced thin pool.
def get_thinpool_data():
    config = parse_serviced_config()
    data = get_serviced_settings(config)
    data.update(get_tpool_stats(config))
    return data


##############################################################################
# After we gather the data, check that we have enough required space to keep
# us out of emergency shutdown mode on upgrade.


# Returns "" if there are no problems, otherwise returns a string explaining
# what was too small.
def check_thinpool():
    stats = get_thinpool_data()
    err = ""
    if stats['data_free'] < stats['data_min_free']:
        err += "\nThe thinpool storage free (%s) is under the minimum threshold (%s)" % \
            (humansize(stats['data_free']), humansize(stats['data_min_free']))
    if stats['meta_free'] < stats['meta_min_free']:
        err += "\nThe thinpool metadata free (%s) is under the minimum threshold (%s)" % \
            (humansize(stats['meta_free']), humansize(stats['meta_min_free']))
    return err


if __name__ == "__main__":
    err = check_thinpool()
    if err:
        print err
