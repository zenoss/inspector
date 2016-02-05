#!/usr/bin/env python

# zenoss-inspector-info

import platform

distro, version, id = platform.linux_distribution()

def bail():
    print "%s %s is not supported. Please use CentOS or Red Hat Linux version 7.1 or greater." % (distro, version)
    import sys; sys.exit(0)

if not 'CentOS' in distro and not 'Red Hat' in distro:
    bail()

vsplit = [int(v) for v in version.split('.')]

if vsplit[0] < 7:
    bail()

if vsplit[1] < 1:
    bail()





