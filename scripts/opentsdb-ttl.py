#!/usr/bin/env python

# zenoss-inspector-info
# zenoss-inspector-tags rm opentsdb ZEN-22981

import subprocess as sp


def run(cmd):
    p = sp.Popen(cmd, stdout=sp.PIPE, stderr=sp.PIPE)
    stdout, stderr = p.communicate()
    if p.returncode != 0:
        raise sp.CalledProcessError(p.returncode, ' '.join(cmd))
    return stdout, stderr


def main():
    cmd = ["serviced", "service", "shell", "writer",
           "bash", "-c", "echo list|/opt/hbase/bin/hbase shell"]
    stdout, stderr = run(cmd)

    # Get the tsdb table names for all tenants
    for line in stdout.strip().split("\n"):
        # Only check tsdb tables
        if line.endswith("-tsdb"):
            # Describe the table
            cmd = ["serviced", "service", "shell", "writer",
                   "bash", "-c",
                   "echo 'describe \"{}\"'|/opt/hbase/bin/hbase shell".format(
                       line)]
            stdout, stderr = run(cmd)

            # Check the TTL
            if ("TTL => 'FOREVER'" in stdout or
                    "TTL => '2147483647'" in stdout):
                print "CHECK FAILED: Tenant {} has opentsdb TTL set " \
                    "to FOREVER".format(line)
                print "Set to 90 days with:"
                print "    serviced service shell writer " \
                    "/opt/opentsdb/set-opentsdb-table-ttl.sh 7776000"

if __name__ == "__main__":
    main()
