#!/usr/bin/env python

# zenoss-inspector-info
# zenoss-inspector-tags docker verify
# zenoss-inspector-deps docker-config.sh

import subprocess as sp

def main():
    cmd = ["ip", "addr", "show", "docker0"]
    p = sp.Popen(cmd, stdout=sp.PIPE, stderr=sp.PIPE)
    stdout, stderr = p.communicate()
    if p.returncode != 0:
        raise sp.CalledProcessError(p.returncode, ' '.join(cmd))
    ipV4InfoLine =  stdout.split('\n')[2].strip()
    ipv4AddrWithNetmask = ipV4InfoLine.split()[1]
    ipv4AddrWithoutNetmask = ipv4AddrWithNetmask.split('/')[0]
    bip = "--bip=" + ipv4AddrWithNetmask
    dns = "--dns=" + ipv4AddrWithoutNetmask
    with open('docker-config.sh.stdout', 'r') as f:
        data = f.read()
    if not dns in data:
        print "/etc/sysconfig/docker missing %s" % dns
    if not bip in data:
        print "/etc/sysconfig/docker missing %s" % bip


if __name__ == "__main__":
    main()
