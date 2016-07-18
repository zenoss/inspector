#!/usr/bin/env python

# zenoss-inspector-info
# zenoss-inspector-tags os verify
# zenoss-inspector-deps serviced-service-list-v.sh

def main():
    with open("serviced-service-list-v.sh.stdout", 'r') as f:
        lines = f.readlines()
    for line in lines:
        if "Startup" and "/opt/zenoss/ZenPacks" in line:
            print 'There is a problem with the Startup line for the following:'
            print line
            print 'To correct this edit the service definition with "serviced service edit SERVICE_NAME"'
            print 'and edit the Startup line to use the symbolic link at "/opt/zenoss/bin"'
if __name__ == "__main__":
    main()
