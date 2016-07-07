#!/usr/bin/env python

# zenoss-inspector-info
# zenoss-inspector-tags docker verify
# zenoss-inspector-deps docker-service.sh

import ConfigParser

def bail():
    print "It doesn't appear /etc/sysconfig/docker has been referenced in your docker.service file."
    import sys; sys.exit()

def bail2():
    print 'Docker configuration should specify "TimeoutSec=300" please adjust in "/etc/systemd/system/docker.service.d/docker.conf", prior to CC 1.1.3 this should be set in /usr/lib/systemd/system/docker.service'
    import sys; sys.exit()

def main():
    config = ConfigParser.RawConfigParser()
    config.read('docker-service.sh.stdout')
    if not config.has_option('Service', 'EnvironmentFile'):
        bail()
    if config.get('Service', 'EnvironmentFile') != '-/etc/sysconfig/docker':
        bail()
    if not config.has_option('Service', 'TimeoutSec'):
        bail2()
    if config.get('Service', 'TimeoutSec') != '300':
        bail2()


if __name__ == "__main__":
    main()
