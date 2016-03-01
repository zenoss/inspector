#!/usr/bin/env python

# zenoss-inspector-info
# zenoss-inspector-tags docker
# zenoss-inspector-deps docker-service.sh

import ConfigParser

def bail():
    print "It doesn't appear /etc/sysconfig/docker has been referenced in your docker.service file."
    import sys; sys.exit()

def main():
    config = ConfigParser.RawConfigParser()
    config.read('docker-service.sh.stdout')
    if not config.has_option('Service', 'EnvironmentFile'):
        bail()
    if config.get('Service', 'EnvironmentFile') != '-/etc/sysconfig/docker':
        bail()

if __name__ == "__main__":
    main()
