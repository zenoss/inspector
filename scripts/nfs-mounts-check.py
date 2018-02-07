#!/usr/bin/env python

# zenoss-inspector-info
# zenoss-inspector-tags os verify
# zenoss-inspector-deps nfs-mounts.sh

def main():
    with open("nfs-mounts.sh.stdout", 'r') as f:
        for line in f.readlines():
            if "Defaultvers" in line:
                if "Defaultvers=4.0" not in line:
                    print "NFS mounts should force the specific version: 4.0."
                    print "See: https://support.zenoss.com/hc/en-us/articles/115005085763-Potential-issues-running-with-RHEL-7-4-or-CentOS-7-4"
                    
    return

if __name__ == "__main__":
    main()
