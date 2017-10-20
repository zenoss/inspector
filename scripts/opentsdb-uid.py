#!/usr/bin/env python

# zenoss-inspector-info
# zenoss-inspector-tags opentsdb INSP-95
# zenoss-inspector-deps serviced-running.sh serviced-service-deployed.sh

from collections import defaultdict
import subprocess as sp
import sys


def run(cmd):
    p = sp.Popen(cmd, stdout=sp.PIPE, stderr=sp.PIPE)
    stdout, stderr = p.communicate()
    if p.returncode != 0:
        if "service not found" in stderr:
            print "The service named 'reader' was not found; skipping check " \
                  "for opentsdb UID. "
            sys.exit(0)
        else:
            raise sp.CalledProcessError(p.returncode, ' '.join(cmd))
    return stdout, stderr


def verify_serviced_is_running():
    with open('serviced-running.sh.stdout', 'r') as f:
        cc_running = f.read().strip()
    if cc_running == "SERVICED_RUNNING=false":
        print "Serviced is not running; skipping check for opentsdb UID."
        sys.exit(0)


def verify_services_are_deployed():
    with open('serviced-service-deployed.sh.stdout', 'r') as f:
        services_deployed = f.read().strip()
    if services_deployed == "SERVICES_DEPLOYED=false":
        print "No Zenoss services deployed; skipping check for opentsdb UID."
        sys.exit(0)


def main():
    verify_serviced_is_running()
    verify_services_are_deployed()

    cmd = ["serviced", "service", "shell", "reader",
           "/opt/opentsdb/build/tsdb", "uid", "--config",
           "/opt/zenoss/etc/opentsdb/opentsdb.conf", "grep", "."]

    stdout, stderr = run(cmd)
    d = defaultdict(list)
    for line in stdout.split("\n"):
        try:
            type, name, id = line.split(" ", 2)
            if name == '\x00:':
                continue
            d["{} {}".format(type, id.strip())].append(name.rstrip(':'))
        except ValueError:
            continue

    multiples = [v for _, v in d.items() if len(v) > 1]

    if len(multiples) > 0:
        print "OpenTSDB UIDs are corrupt. There multiple mappings for {} ids."\
            .format(len(multiples))


if __name__ == "__main__":
    main()



