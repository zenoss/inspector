#!/usr/bin/env python

# zenoss-inspector-info
# zenoss-inspector-deps systemctl-status.sh
# zenoss-inspector-tags docker serviced


class SystemService(object):
    def __init__(self, name="", description="", loaded=False, active=False, enabled=False):
        self.name = name
        self.description = description
        # self.installed = installed
        self.loaded = loaded
        self.active = active
        self.enabled = enabled

    def validateEnabledAndActive(self):
        if not self.enabled:
            print "System service '%s: %s' is not enabled to start at boot time" % (self.name, self.description)
        if not (self.loaded or self.active):
            print "System service '%s': %s' is not running" % (self.name, self.description)

    def validateDisabledAndStopped(self):
        if self.enabled:
            print "System service '%s': %s' is enabled to start at boot time" % (self.name, self.description)
        if self.active:
            print "System service '%s': %s' is running" % (self.name, self.description)

#
# Parse the contents of systemctl-status.sh.stdout into a list of SystemService objects,
# and verify the status of the services that Control Center does or does not expect to
# be started and running.
#
def main():
    with open("systemctl-status.sh.stdout", 'r') as f:
        lines = f.readlines()

    # Parse the status output into a list of SystemService objects
    services = []
    for line in lines:
        line = line.strip()
        nameValuePair = line.split("=")
        if line.startswith("Names="):
            service = SystemService(nameValuePair[1])
            services.append(service)
        elif line.startswith("Description="):
            service.description = nameValuePair[1]
        elif line.startswith("LoadState="):
            service.loaded = nameValuePair[1] == "loaded"
        elif line.startswith("ActiveState="):
            service.active = nameValuePair[1] == "active"
        elif line.startswith("UnitFileState="):
            service.enabled = nameValuePair[1] == "enabled" or nameValuePair[1] == "static"

    # Verify the service states CC expects
    dnsmasqInstalled = dockerInstalled = ntpInstalled = servicedInstalled = False
    for service in services:
        if service.name.startswith("dnsmasq"):
            dnsmasqInstalled = True
            service.validateEnabledAndActive()
        elif service.name.startswith("docker"):
            dockerInstalled = True
            service.validateEnabledAndActive()
        elif service.name.startswith("firewalld"):
            service.validateDisabledAndStopped()
        elif service.name.startswith("ntp"):
            ntpInstalled = True
            service.validateEnabledAndActive()
        elif service.name.startswith("serviced"):
            servicedInstalled = True
            service.validateEnabledAndActive()

    if not dnsmasqInstalled:
        print "The dnsmasq service is not installed"

    if not dockerInstalled:
        print "The docker service is not installed"

    if not ntpInstalled:
        print "The ntp service is not installed"

    if not servicedInstalled:
        print "The Control Center service is not installed"

if __name__ == "__main__":
    main()
