#!/usr/bin/env python

# zenoss-inspector-info
# zenoss-inspector-tags os
# zenoss-inspector-deps df.sh

CUTOFF = 90

def main():
    with open("df.sh.stdout", 'r') as f:
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
        print "The following filesystems are >= %d%% full:" % CUTOFF
        print lines[0].strip()
        for line in full:
            print line.strip()

if __name__ == "__main__":
    main()
