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
# Converts human readable numbers to and from numbers.
#
##############################################################################

import re
import sys

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

# Not the most intuitive regular expression.  Groups here will be:
# group(1): None or "-" for negative numbers
# group(2): The numeric part of the string, ie "10.3"
# group(3): [unused] the decimal portion for floats, ie ".3"
# group(4): (The first letter denoting the unit "G", "k", "M", etc)
# group(5): None or "i" if this is given in binary abbreviations. If provided
#           then group(4) is forced lowercase (10 GiB is translatd to 10 gb)
#           for the purpose of looking up the value in the SIZES dictionary.
# group(6): None, "b", or "B".  Will always be "b" for SIZES lookups.
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
    """
    Takes a number, a base (ie: 1000 for humansize or 1024 for
    bytesize), and a map of abbreviations for the steps.  Returns
    the number rounded to 3 decimal places matched to the abbreviation
    it falls into.  See the comments in humansize() and bytesize()
    for examples of the output.
    """
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


def __test():
    """
    Make sure a round-trip conversions works.

    >>> parse_size(humansize(0))
    0.0
    >>> parse_size(humansize(10000))
    10000.0
    >>> parse_size(bytesize(1024*1024*1024))
    1073741824.0
    """
    pass


if __name__ == '__main__':
    import doctest
    # If run, make sure test cases pass.
    doctest.testmod()

