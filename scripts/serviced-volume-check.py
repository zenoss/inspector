#!/usr/bin/env python

# zenoss-inspector-info
# zenoss-inspector-tags os verify
# zenoss-inspector-deps serviced-storage.sh storage-config.sh
import re

def main():
    with open("serviced-storage.sh.stdout", 'r') as f:
        lines = f.readlines()
    for line in lines:
        if "Application Data" in line:
            volId = line.split()[0]
            path = "/opt/serviced/var/volumes/.devicemapper/volumes/" + volId + "/metadata.json"
            with open(path, 'r') as f2:
                line = f2.readline()
                pattern = re.compile('^\{\"CurrentDevice\"\:\"(?P<blkId>\w*)')
                pool = pattern.match(line).group('blkId')

            with open("storage-config.sh.stdout", 'r') as f:
                lines = f.readlines()
                for line in lines:
                    if "opt/serviced/var/volumes" in line:
                        print "Storage volume mismatch on serviced-serviced--pool: %s see lsblk output for more information CC-2487" % pool


if __name__ == "__main__":
    main()
