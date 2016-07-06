#!/usr/bin/env python

# zenoss-inspector-info
# zenoss-inspector-deps serviced-config.sh serviced-storage.sh
import os
from stat import *

def main():
    with open("serviced-config.sh.stdout", 'r') as f:
        lines = f.readlines()

    isMaster = False
    fs_type = "devicemapper"
    thinpool_device = ""
    for line in lines:
        line = line.strip()
        if line.startswith("#"):
            continue

        split = line.split("=")
        if split[0] == "SERVICED_FS_TYPE":
            fs_type = split[1]
        elif split[0] == "SERVICED_DM_THINPOOLDEV":
            thinpool_device = split[1]
        elif split[0] == "SERVICED_MASTER":
            isMaster = split[1] in ("1", "true", "t", "yes")

    if fs_type != "devicemapper":
        print ("serviced is configured to use a filesystem of type '%s', but 'devicemapper' is recommended." % fs_type)
    elif isMaster and not thinpool_device:
        print ("serviced is configured to use devicemapper, but SERVICED_DM_THINPOOLDEV is not defined")

    with open("serviced-storage.sh.stdout", 'r') as f:
        lines = f.readlines()
        for line in lines:
            if "Application Data" in line:
                subVolumePath = "/opt/serviced/var/volumes/" + line.split()[0]
                for d in range(1,4):
                    path = subVolumePath + "/hbase-zookeeper-" + str(d)
                    if oct(os.stat(path)[ST_MODE])[-3:] != "755" or os.stat(path)[ST_UID] != 102 or os.stat(path)[ST_GID] != 105:
                        print 'Permision or ownership is incorrect on: %s' % subVolumePath + "/hbase-zookeeper-" + str(d)
                        print 'hbase-zookeeper-* directory permissions and ownership should be: "drwxr-xr-x 2  102  105"'


if __name__ == "__main__":
    main()
