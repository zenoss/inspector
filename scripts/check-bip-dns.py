#!/usr/bin/env python

# zenoss-inspector-info
# zenoss-inspector-tags docker
# zenoss-inspector-deps docker-config.sh

import subprocess as sp

def main():
    cmd = ["ip", "addr", "show", "docker0"]
    p = sp.Popen(cmd, stdout=sp.PIPE, stderr=sp.PIPE)
    stdout, stderr = p.communicate()
    if p.returncode != 0:
        raise sp.CalledProcessError(p.returncode, ' '.join(cmd))
    bip = "--bip=" + stdout.split('\n')[2].strip().split()[1]
    dns = "--dns=" + stdout.split('\n')[2].strip().split()[1].split('/')[0]
    with open('docker-config.sh.stdout', 'r') as f:
        data = f.read()
    if not dns in data:
        print "/etc/sysconfig/docker missing %s" % dns
    if not bip in data:
        print "/etc/sysconfig/docker missing %s" % bip


if __name__ == "__main__":
    main()
