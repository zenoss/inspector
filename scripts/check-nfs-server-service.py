#!/usr/bin/env python

# zenoss-inspector-deps nfs-server-service.sh serviced-version.sh
# zenoss-inspector-info


def main():
    with open('serviced-version.sh.stdout') as vfile:
        cc_version = vfile.read().replace('\n', '')

    if cc_version == "1.0" or cc_version == "1.1":
        conf_file="/lib/systemd/system/nfs-server.service"
    elif cc_version == "1.2":
        conf_file="/etc/systemd/system/nfs-server.service.d/nfs-server.conf"
    else:
        conf_file="nfs-server config"

    with open('nfs-server-service.sh.stdout', 'r') as f:
        lines = f.readlines()
    foundTarget = False
    foundService = False
    for line in lines:
        if 'Requires' in line and 'rpcbind.target' in line:
            foundTarget = True
        if 'Requires' in line and 'rpcbind.service' in line:
            foundService = True
    if foundTarget and not foundService:
        print 'It appears rpcbind.target has been required in your %s file. Instead, require rpcbind.service.' % conf_file
    if foundTarget and foundService:
        print 'It appears rpcbind.target and rpcbind.service have both been required in your %s file. Require only rpcbind.service.' % conf_file
    if not foundTarget and not foundService:
        print 'Require rpcbind.service in your %s file.' % conf_file
    
    
if __name__ == '__main__':
    main()
