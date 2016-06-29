#!/usr/bin/env python

# zenoss-inspector-info
# zenoss-inspector-deps uname-a.sh
import re

def main():
    with open("uname-a.sh.stdout", 'r') as f:
        line = f.read()
        if tuple(map(int, re.search(r'^[^ ]+ [^ ]+ (\d+)\.(\d+)\.(\d+)-(\d+)', line).groups())) < (3,10,0,327):
            print 'Kernel version must be 3.10.0-327 or higher, please update your kernel'

if __name__ == "__main__":
    main()
