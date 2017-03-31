#!/usr/bin/env python

# zenoss-inspector-info
# zenoss-inspector-tags network serviced-delegate verify
# zenoss-inspector-deps etchosts.sh

def main():
    with open("etchosts.sh.stdout", 'r') as f:
        lines = f.readlines()
    for line in lines:
        split = line.split()
        if "127.0.0.1" in split and "localhost" in split:
            return
    print ("You don't appear to have a mapping for localhost to 127.0.0.1 in "
           "your /etc/hosts file.")

if __name__ == "__main__":
    main()
