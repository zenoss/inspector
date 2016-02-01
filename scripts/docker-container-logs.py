#!/usr/bin/env python

# zenoss-inspector-tags slow docker

import subprocess as sp
import json

def main():
    cmd = ["docker", "ps", "-a", "--no-trunc", "-q"]
    p = sp.Popen(cmd, stdout=sp.PIPE, stderr=sp.PIPE)
    stdout, stderr = p.communicate()
    if p.returncode != 0:
        raise sp.CalledProcessError(p.returncode, ' '.join(cmd))
    logs = {}
    for cid in stdout.strip().split("\n"):
        cmd = ["docker", "logs", "-t", cid]
        p = sp.Popen(cmd, stdout=sp.PIPE, stderr=sp.PIPE)
        stdout, stderr = p.communicate()
        logs[cid] = stdout
    print json.dumps(logs)
    for cid, lines in logs.iteritems():
        print "\n" * 2
        print "zenoss inspector container logs: %s" % cid
        print "=" * 80
        print lines

if __name__ == "__main__":
    main()
