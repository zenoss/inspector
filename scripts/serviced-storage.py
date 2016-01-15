#!/usr/bin/env python

# zenoss-inspector-info
# zenoss-inspector-deps serviced-confg.sh

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

if __name__ == "__main__":
    main()
