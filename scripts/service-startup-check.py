#!/usr/bin/env python

# zenoss-inspector-info
# zenoss-inspector-tags verify
# zenoss-inspector-deps serviced-service-list-v.sh
import json
import os
import sys
from pprint import pprint

def main():
    data_file_name = 'serviced-service-list-v.sh.stdout'
    if os.path.getsize(data_file_name) == 0:
        print "Skipping this check because no services are deployed"
        sys.exit(0)

    with open(data_file_name) as data_file:
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
