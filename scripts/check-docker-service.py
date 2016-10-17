#!/usr/bin/env python

# zenoss-inspector-info
# zenoss-inspector-tags docker verify
# zenoss-inspector-deps docker-service.sh

import ConfigParser

service_file = "/etc/systemd/system/docker.service.d/docker.conf"


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

    # The value of
    if not config.has_option('Service', 'ExecStart'):
        print "'ExecStart' directive is missing from {}".format(service_file)
    else:
        startCmd = config.get('Service', 'ExecStart')
        if "$OPTIONS" not in startCmd:
            print "'ExecStart' directive missing $OPTIONS. Update {}".format(service_file)

if __name__ == "__main__":
    main()
