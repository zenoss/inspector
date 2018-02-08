#!/usr/bin/env python

# zenoss-inspector-info
# zenoss-inspector-tags os verify
# zenoss-inspector-deps nfs-mounts.sh

def main():

    DefaultVersion = ""
    ActiveVersion = ""

    with open("nfs-mounts.sh.stdout", 'r') as f:
        for line in f.readlines():
            if "Defaultvers=" not in line:
                continue
            line = line.strip()
            version = line.split("Defaultvers=",1)[1]
            if line.startswith("#"): 
                DefaultVersion = version
            else:
                ActiveVersion = version

    if "4.0" not in DefaultVersion and "4.0" not in ActiveVersion:
                    print "NFS mounts should force the specific version: 4.0."
                    print "Default version is set to '%s' and override version is set to '%s'" % (DefaultVersion, ActiveVersion)
                    print "See: https://support.zenoss.com/hc/en-us/articles/115005085763-Potential-issues-running-with-RHEL-7-4-or-CentOS-7-4"
    return

if __name__ == "__main__":
    main()
