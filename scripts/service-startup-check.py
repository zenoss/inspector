#!/usr/bin/env python

# zenoss-inspector-info
# zenoss-inspector-tags verify
# zenoss-inspector-deps serviced-running.sh serviced-service-deployed.sh serviced-service-list-v.sh

import json
import sys

from pprint import pprint

def main():
    cc_running = ""
    with open('serviced-running.sh.stdout', 'r') as f:
        cc_running = f.read().strip()
    if cc_running == "SERVICED_RUNNING=false":
        print "Serviced is not running; skipping check for service startup commands."
        sys.exit(0)

    services_deployed = ""
    with open('serviced-service-deployed.sh.stdout', 'r') as f:
        services_deployed = f.read().strip()
    if services_deployed == "SERVICES_DEPLOYED=false":
        print "No Zenoss services deployed; skipping check for service startup commands."
        sys.exit(0)

    with open('serviced-service-list-v.sh.stdout') as data_file:
        data = json.load(data_file)
        #pprint(data)
        for i in data:
            if "/opt/zenoss/ZenPacks" in i["Startup"]:
                print "There is an issue with the Startup command for %s" % i["Name"]
                print i["Startup"]
                print 'To correct this you should edit the service definition',\
                      'with "serviced service edit %s" changing the Startup' % i["Name"], \
                      'line to use the symbolic link at "/opt/zenoss/bin/%s"' % i["Name"]

if __name__ == "__main__":
    main()
