#!/usr/bin/env python

# zenoss-inspector-info
# zenoss-inspector-tags opentsdb INSP-95
# zenoss-inspector-deps serviced-running.sh serviced-service-deployed.sh

import subprocess as sp
import sys
from collections import defaultdict


def run_tsdb_cmd():
    """Run OpenTSDB command to get UID information."""
    cmd = ["serviced", "service", "shell", "reader",
           "/opt/opentsdb/build/tsdb", "uid", "--config",
           "/opt/zenoss/etc/opentsdb/opentsdb.conf", "grep", "."]

    p = sp.Popen(cmd, stdout=sp.PIPE, stderr=sp.PIPE)
    stdout, stderr = p.communicate()
    if p.returncode != 0:
        if "service not found" in stderr:
            print "The service named 'reader' was not found; skipping check " \
                  "for OpenTSDB UID corruption."
            sys.exit(0)
        else:
            raise sp.CalledProcessError(p.returncode, ' '.join(cmd))
    return stdout, stderr


def verify_serviced_is_running():
    """Make sure serviced is running. If not, print error and exit."""
    with open('serviced-running.sh.stdout', 'r') as f:
        cc_running = f.read().strip()
    if cc_running == "SERVICED_RUNNING=false":
        print "Serviced is not running; skipping check for OpenTSDB UID " \
              "corruption. "
        sys.exit(0)


def verify_services_are_deployed():
    """Make sure services are deployed. If not, print error and exit."""
    with open('serviced-service-deployed.sh.stdout', 'r') as f:
        services_deployed = f.read().strip()
    if services_deployed == "SERVICES_DEPLOYED=false":
        print "No Zenoss services deployed; skipping check for OpenTSDB UID " \
              "corruption. "
        sys.exit(0)


def main():
    """Check for double-mapped OpenTSDB UIDs. Warn user if corrupted."""
    verify_serviced_is_running()
    verify_services_are_deployed()

    stdout, _ = run_tsdb_cmd()

    d = defaultdict(list)
    for line in stdout.split("\n"):
        try:
            kind, name, uid = line.split(" ", 2)
            if name == '\x00:':
                continue
            d["{} {}".format(kind, uid.strip())].append(name.rstrip(':'))
        except ValueError:
            continue

    multiples = [v for _, v in d.items() if len(v) > 1]
    mc = len(multiples)
    if mc > 0:
        print "OpenTSDB UIDs are corrupt. There are {} UIDs with multiple " \
              "mappings. Contact Zenoss support for assistance.".format(mc)


if __name__ == "__main__":
    main()
