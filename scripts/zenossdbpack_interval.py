#!/usr/bin/env python

# zenoss-inspector-deps zenossdbpack_cron.sh
# zenoss-inspector-tags config serviced serviced-delegate verify
# zenoss-inspector-info

import re
regex = re.compile("\*\ [a-zA-Z0-9_.-]*\ root")
def main():
    results = 0
    with open('zenossdbpack_cron.sh.stdout') as cronfile:
        for line in cronfile:
            if regex.search(line):
                results = results +1
                if results > 0:
                    print "Zenoss recommends changing your zenossdbpack interval do daily in /etc/cron.d/cron_zenossdbpack:"
                    print "Example daily at midnight:"
                    print "0 0 * * * root /opt/serviced/bin/serviced-zenossdbpack"

if __name__ == "__main__":
    main()
