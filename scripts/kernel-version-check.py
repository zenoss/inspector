#!/usr/bin/env python

# zenoss-inspector-info
# zenoss-inspector-tags os
# zenoss-inspector-deps uname-a.sh

import re
import platform

def main():
    # Check for Centos/RHEL 7.2
    if tuple(map(int, platform.linux_distribution()[1].split('.'))) >= (7,2):
        with open("uname-a.sh.stdout", 'r') as f:
            line = f.read()
            kver = tuple(map(int, re.search(r'^[^ ]+ [^ ]+ (\d+)\.(\d+)\.(\d+)-(\d+)', line).groups())) 
            if (3,10,0,229) < kver < (3,10,0,327):        
                print 'Kernel versions between 3.10.0-229 and 3.10.0-327 do not support fstrim which is used to free unused storage blocks over time. Update to version 3.10.0-327 or higher to avoid running out of usable storage'

if __name__ == "__main__":
    main()
