#!/usr/bin/env python

# zenoss-inspector-info
# zenoss-inspector-tags os verify
# zenoss-inspector-deps serviced-storage.sh storage-config.sh


def main():
    with open("serviced-storage.sh.stdout", 'r') as f:
        lines = f.readlines()
    for line in lines:
        if "Application Data" in line:
            volumeId = line.split()[0]
            print volumeId

    with open("storage-config.sh.stdout", 'r') as f:
        lines = f.readlines()
    for line in lines:
        if "/opt/serviced/var/volumes/" in line:
            print "Storage volume mismatch see lsblk output for further information"


if __name__ == "__main__":
    main()
