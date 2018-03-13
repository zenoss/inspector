#!/usr/bin/env python

# zenoss-inspector-info
# zenoss-inspector-tags mariadb verify

import re
import json
import shlex
import subprocess

def main():
    modelprocess = subprocess.Popen(shlex.split("serviced service list mariadb-model"), stdout=subprocess.PIPE)
    modeloutput = json.loads(modelprocess.stdout.read())
    modelcontent = modeloutput["ConfigFiles"]["/etc/my.cnf"]["Content"]
    modelmaxvalue  =  float(re.search(r"max_connections\s*=\s*'*\"*(\d+)", modelcontent).group(1))
    if modelmaxvalue < 1000:
        print "Max Connections Value for MariaDB-model is too low, Zenoss recommends a minimum value of 1000"
        print "See: https://support.zenoss.com/hc/en-us/articles/208205873-Database-Tuning-and-Optimization-for-zends-mysql-mariadb "
    eventsprocess = subprocess.Popen(shlex.split("serviced service list mariadb-events"), stdout=subprocess.PIPE)
    eventsoutput = json.loads(eventsprocess.stdout.read())
    eventscontent = eventsoutput["ConfigFiles"]["/etc/my.cnf"]["Content"]
    eventsmaxvalue = float(re.search(r"max_connections\s*=\s*'*\"*(\d+)", eventscontent).group(1))
    if eventsmaxvalue < 1000:
        print "Max Connections Value for MariaDB-events is too low, Zenoss recommends a minimum value of 1000"
        print "See: https://support.zenoss.com/hc/en-us/articles/208205873-Database-Tuning-and-Optimization-for-zends-mysql-mariadb "
    return

if __name__ == "__main__":
    main()
