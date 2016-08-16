#!/usr/bin/env python

# zenoss-inspector-info
# zenoss-inspector-tags rm opentsdb verify ZEN-22981

import subprocess as sp

# Shell commands to access opentsdb containers
opentsdb_containers = {
    "internal": ["docker", "exec", "serviced-isvcs_opentsdb"],
    "Resource Manager": ["serviced", "service", "shell", "writer"],
}


def run(cmd):
    print "Running '{}'...".format(cmd)
    p = sp.Popen(cmd, stdout=sp.PIPE, stderr=sp.PIPE)
    stdout, stderr = p.communicate()
    if p.returncode != 0:
        raise sp.CalledProcessError(p.returncode, ' '.join(cmd))
    return stdout, stderr


def main():
    for service, command in opentsdb_containers.iteritems():
        cmd = command + ["bash", "-c", "echo list|/opt/hbase/bin/hbase shell"]
        stdout, stderr = run(cmd)

        # Get the tsdb table names for all tenants
        for line in stdout.strip().split("\n"):
            # Only check tsdb tables
            if line.endswith("tsdb"):
                # Describe the table
                cmd = command + ["bash", "-c",
                    "echo 'describe \"{}\"'|/opt/hbase/bin/hbase shell".format(
                        line)]
                stdout, stderr = run(cmd)

                # Check the TTL
                if ("TTL => 'FOREVER'" in stdout or
                        "TTL => '2147483647'" in stdout):
                    print "CHECK FAILED: Tenant {} ({}) has opentsdb TTL " \
                        "set to FOREVER".format(line, service)
                    print "Set to 90 days with:"
                    print "    {} " \
                        "/opt/opentsdb/set-opentsdb-table-ttl.sh" \
                        "7776000".format(command)

if __name__ == "__main__":
    main()
