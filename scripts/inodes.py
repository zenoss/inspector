#!/usr/bin/env python

# zenoss-inspector-info
# zenoss-inspector-tags os
# zenoss-inspector-deps dfinode.sh

CUTOFF = 90

def main():
    with open("dfinode.sh.stdout", 'r') as f:
        lines = f.readlines()
    full = []
    for line in lines[1:]:
        try:
            pct = int(line.split()[5].replace('%', ''))
        except ValueError:
            continue
        if pct >= CUTOFF:
            full.append(line)
    if len(full) > 0:
        print "The following filesystems are using >= %d%% of their inodes:" % CUTOFF
        print lines[0].strip()
        for line in full:
            print line.strip()

if __name__ == "__main__":
    main()
