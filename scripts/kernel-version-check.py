#!/usr/bin/env python

# zenoss-inspector-info
# zenoss-inspector-deps uname-a.sh
import re
import platform

def main():
    # Check for Centos/RHEL 7.2
    if tuple(map(int, platform.linux_distribution()[1].split('.'))) >= (7,2):
        with open("uname-a.sh.stdout", 'r') as f:
            line = f.read()
            kver = tuple(map(int, re.search(r'^[^ ]+ [^ ]+ (\d+)\.(\d+)\.(\d+)-(\d+)', line).groups())) 
            if kver < (3,10,0,327):
                if kver > (3,10,0,229):
                    print 'Kernel version does not support fstrim, update to version 3.10.0-327 or higher'

if __name__ == "__main__":
    main()
