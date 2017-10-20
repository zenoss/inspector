#!/usr/bin/env python

# zenoss-inspector-info
# zenoss-inspector-tags opentsdb INSP-95
# zenoss-inspector-deps serviced-running.sh serviced-service-deployed.sh

from collections import defaultdict
import subprocess as sp
import sys

# def get_cc_running():
#     cc_running = ""
#     with open('serviced-running.sh.stdout', 'r') as f:
#         cc_running = f.read().strip()
#     return cc_running
#
# def get_services_deployed():
#     services_deployed = ""
#     with open('serviced-service-deployed.sh.stdout', 'r') as f:
#         services_deployed = f.read().strip()
#     return services_deployed


def run(cmd):
    p = sp.Popen(cmd, stdout=sp.PIPE, stderr=sp.PIPE)
    stdout, stderr = p.communicate()
    if p.returncode != 0:
        if "service not found" in stderr:
            print "The service named 'writer' was not found; skipping check " \
                  "for opentsdb TTL. "
            sys.exit(0)
        else:
            raise sp.CalledProcessError(p.returncode, ' '.join(cmd))
    return stdout, stderr


def serviced_is_running():
    with open('serviced-running.sh.stdout', 'r') as f:
        cc_running = f.read().strip()
    if cc_running == "SERVICED_RUNNING=false":
        return False
    return True



def services_are_deployed():
    with open('serviced-service-deployed.sh.stdout', 'r') as f:
        services_deployed = f.read().strip()
    if services_deployed == "SERVICES_DEPLOYED=false":
        print "No Zenoss services deployed; skipping check for opentsdb TTL."
        sys.exit(0)
    return True


def main():
    if not serviced_is_running():
        print "Serviced is not running; skipping check for opentsdb UID."
        sys.exit(0)

    if not services_are_deployed():
        print "No Zenoss services deployed; skipping check for opentsdb UID."
        sys.exit(0)

    print "Opentsdb UID check can continue - serviced is running and " \
          "services are deployed. "

    cmd = ["serviced", "service", "attach", "reader",
           "/opt/opentsdb/build/tsdb", "uid", "--config",
           "/opt/zenoss/etc/opentsdb/opentsdb.conf", "grep", "."]
    stdout, stderr = run(cmd)
    d = defaultdict(list)
    for line in stdout.split("\n"):
        try:
            type, name, id = line.split(" ", 2)
            # import pdb; pdb.set_trace()
            if name == '\x00:':
                # print "skipping: [{}, {}, {}]".format(type, name, id)
                continue
            d["{} {}".format(type, id.strip())].append(name.rstrip(':'))
            # print "type: {}\tname: {}\tid: {}".format(type, name, id)
        except ValueError:
            print "ValueError splitting line: {}".format(line)
        # print "line: {}\n".format(line)

    multiples = [v for _,v in d.items() if len(v) > 1]
    singles = [v for _,v in d.items() if len(v) == 1]
    print "{} multiple-mapped ids and {} single-mapped ids were found".format(len(multiples), len(singles))


    # print "STDOUT:\n=======\n{}\n".format(stdout)
    print "\nSTDERR:\n=======\n{}\n".format(stderr)

if __name__ == "__main__":
    main()



