#!/usr/bin/env python

# zenoss-inspector-info
# zenoss-inspector-tags mariadb verify

import json
import shlex
import subprocess

def main():
    modelprocess = subprocess.Popen(shlex.split("serviced service list mariadb-model"), stdout=subprocess.PIPE)
    modeloutput = json.loads(modelprocess.stdout.read())
    modelcontent = modeloutput["ConfigFiles"]["/etc/my.cnf"]["Content"]
    if "max_connections = 500" in modelcontent:
        print "Max Connections Value for MariaDB-model is too low, Zenoss recommends a minimum value of 1000"
        print "See: https://support.zenoss.com/hc/en-us/articles/208205873-Database-Tuning-and-Optimization-for-zends-mysql-mariadb "
    eventsprocess = subprocess.Popen(shlex.split("serviced service list mariadb-events"), stdout=subprocess.PIPE)
    eventsoutput = json.loads(eventsprocess.stdout.read())
    eventscontent = eventsoutput["ConfigFiles"]["/etc/my.cnf"]["Content"]
    if "max_connections = 500" in eventscontent:
        print "Max Connections Value for MariaDB-events is too low, Zenoss recommends a minimum value of 1000"
        print "See: https://support.zenoss.com/hc/en-us/articles/208205873-Database-Tuning-and-Optimization-for-zends-mysql-mariadb "
    return

if __name__ == "__main__":
    main()
