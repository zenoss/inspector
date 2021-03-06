#!/usr/bin/env python

# zenoss-inspector-info
# zenoss-inspector-tags docker verify
# zenoss-inspector-deps docker-config.sh

import subprocess as sp

service_file = "/etc/systemd/system/docker.service.d/docker.conf"
config_file = "/etc/sysconfig/docker"

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

    cgroupdriver="--exec-opt native.cgroupdriver=cgroupfs"
    thinpoolStorageopt="--storage-opt dm.thinpooldev=/dev/mapper/docker-docker--pool"
    discardStorageopt="--storage-opt dm.mountopt=discard"

    with open('docker-config.sh.stdout', 'r') as f:
        data = f.read()

    if not dns in data:
        print "The docker daemon configuration for '--dns' is missing or incorrect"
        print "The correct value is '%s'" % dns
        print "Please add the correct value to the 'OPTIONS=' directive in %s" % config_file
        print "And make sure that there are no additional '--dns' arguments specified in the 'ExecStart=' directive in %s" % service_file

    if not bip in data:
        print "The docker daemon configuration for '--bip' is missing or incorrect"
        print "The correct value is '%s'" % bip
        print "Please add the correct value to the 'OPTIONS=' directive in %s" % config_file
        print "And make sure that there are no additional '--bip' arguments specified in the 'ExecStart=' directive in %s" % service_file

    if not cgroupdriver in data:
        print "The docker daemon configuration for '--exec-opt native.cgroupdriver=' is missing or incorrect"
        print "The correct value is '%s'" % cgroupdriver
        print "Please add the correct value to the 'OPTIONS=' directive in %s" % config_file
        print "And make sure that there are no additional '--exec-opt' arguments specified in the 'ExecStart=' directive in %s" % service_file

    if not thinpoolStorageopt in data:
        print "The docker daemon configuration for '--storage-opt dm.thinpooldev=' is missing or incorrect"
        print "The correct value is '%s'" % thinpoolStorageopt
        print "Please add the correct value to the 'OPTIONS=' directive in %s" % config_file
        print "And make sure that there are no additional '----storage-opt' arguments specified in the 'ExecStart=' directive in %s" % service_file

    if not discardStorageopt in data:
        print "The docker daemon configuration for '--storage-opt dm.mountopt=' is missing or incorrect"
        print "The correct value is '%s'" % discardStorageopt
        print "Please add the correct value to the 'OPTIONS=' directive in %s" % config_file
        print "And make sure that there are no additional '----storage-opt' arguments specified in the 'ExecStart=' directive in %s" % service_file

if __name__ == "__main__":
    main()
