#!/usr/bin/env python

# zenoss-inspector-info
# zenoss-inspector-tags verify
# zenoss-inspector-deps serviced-storage.sh storage-config.sh


def main():
    with open("serviced-storage.sh.stdout", 'r') as f:
        lines = f.readlines()
    for line in lines:
        if "Application Data" in line:
            volId = line.split()[0]
            with open("/opt/serviced/var/volumes/.devicemapper/volumes/$volId/metadata.json")


    with open("storage-config.sh.stdout", 'r') as f:
        lines = f.readlines()
    for line in lines:
        if "/opt/serviced/var/volumes/" in line:
            print "Storage volume mismatch see lsblk output for further information"


if __name__ == "__main__":
    main()
