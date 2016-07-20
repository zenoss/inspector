#!/usr/bin/env python

# zenoss-inspector-info
# zenoss-inspector-tags verify
# zenoss-inspector-deps serviced-service-list-v.sh
import json
from pprint import pprint

def main():
    with open('serviced-service-list-v.sh.stdout') as data_file:
        data = json.load(data_file)
        #pprint(data)
        for i in data:
            if "/opt/zenoss/ZenPacks" in i["Startup"]:
                print "There is an issue with Startup command %s" % i["Name"]
                print i["Startup"]
                print 'To correct this you should edit the service definition',\
                      'with "serviced service edit %s" changing the Startup' % i["Name"], \
                      'line to use the symbolic link at "/opt/zenoss/bin/%s"' % i["Name"]

if __name__ == "__main__":
    main()
