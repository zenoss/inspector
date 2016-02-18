#!/usr/bin/env python

# zenoss-inspector-deps nfs-server-service.sh
# zenoss-inspector-info

def main():
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
        print 'It appears rpcbind.target has been required in your /lib/systemd/system/nfs-server.service file. Instead, require rpcbind.service.'
    if foundTarget and foundService:
        print 'It appears rpcbind.target and rpcbind.service have both been required in your /lib/systemd/system/nfs-server.service file. Require only rpcbind.service.'
    if not foundTarget and not foundService:
        print 'Require rpcbind.service in your /lib/systemd/system/nfs-server.service file.'
        
    
    
if __name__ == '__main__':
    main()