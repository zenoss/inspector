#!/usr/bin/env python

# zenoss-inspector-info
# zenoss-inspector-tags docker verify
# zenoss-inspector-deps docker-service.sh

import ConfigParser

service_file = "/lib/systemd/system/docker.service"


def main():
    config = ConfigParser.RawConfigParser()
    config.read('docker-service.sh.stdout')

    # EnvironmentFile
    if not config.has_option('Service', 'EnvironmentFile') or \
            config.get('Service',
                       'EnvironmentFile') != '-/etc/sysconfig/docker':
        print "'EnvironmentFile' directive missing or invalid, add " \
            "'EnvironmentFile=-/etc/sysconfig/docker' to the " \
            "'Service' section in {}".format(service_file)

    # TimeoutSec
    if not config.has_option('Service', 'TimeoutSec') or \
            config.get('Service', 'TimeoutSec') != '300':
        print "'TimeoutSec' directive missing or invalid, add " \
            "'TimeoutSec=300' to the 'Service' section in " \
            "{}".format(service_file)

    # ExecStart
    if not config.has_option('Service', 'ExecStart') or \
            config.get('Service', 'ExecStart') != \
            '/usr/bin/docker daemon $OPTIONS -H fd://':
        print "'ExecStart' directive missing or invalid, add " \
            "'ExecStart=/usr/bin/docker daemon $OPTIONS -H fd://' " \
            "to the 'Service' section in " \
            "{}".format(service_file)

    # TasksMax
    if not config.has_option('Service', 'TasksMax') or \
            config.get('Service', 'TasksMax') != 'infinity':
        print "'TasksMax' directive missing or invalid, add " \
            "'TasksMax=infinity' to the 'Service' section in " \
            "{}".format(service_file)

if __name__ == "__main__":
    main()
