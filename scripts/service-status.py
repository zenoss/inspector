#!/usr/bin/env python

# zenoss-inspector-info
# zenoss-inspector-deps systemctl-status.sh get-ha-versions.sh
# zenoss-inspector-tags docker serviced serviced-worker verify ha

def print_time_sync_warning():
    print "Please ensure you have some form of time synchronization in place on all hosts"
    print "in your Zenoss environment."
    print "If you have some other form of time synchronization in place, for instance a"
    print "time-sync on your hypervisor, then it is safe to ignore this warning."


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
            if self.name.startswith("ntp"):
                print_time_sync_warning()
        if not (self.loaded or self.active):
            print "System service '%s': %s' is not running" % (self.name, self.description)
            if self.name.startswith("ntp"):
                print_time_sync_warning()

    def validateDisabledAndStopped(self):
        if self.enabled:
            print "System service '%s': %s' is enabled to start at boot time" % (self.name, self.description)
        if self.active:
            print "System service '%s': %s' is running" % (self.name, self.description)

# Returns True if the current system is configured for HA
def checkForHA():
    isHA = False
    with open("get-ha-versions.sh.stdout", 'r') as f:
        lines = f.readlines()

    for line in lines:
        line = line.strip()
        if line == "HAS_PCS=true":
            isHA = True
            break

    return isHA
#
# Parse the contents of systemctl-status.sh.stdout into a list of SystemService objects,
# and verify the status of the services that Control Center does or does not expect to
# be started and running.
#
def main():
    isHA = checkForHA()
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
    dnsmasqInstalled = dockerInstalled = ntpInstalled = servicedInstalled = corosyncInstalled = pacemakerInstalled = False
    for service in services:
        if service.name.startswith("dnsmasq"):
            dnsmasqInstalled = True
            service.validateEnabledAndActive()
        elif service.name.startswith("firewalld"):
            service.validateDisabledAndStopped()
        elif service.name.startswith("ntp"):
            ntpInstalled = True
            service.validateEnabledAndActive()
        elif not isHA:
            if service.name.startswith("docker"):
                dockerInstalled = True
                service.validateEnabledAndActive()
            elif service.name.startswith("serviced"):
                servicedInstalled = True
                service.validateEnabledAndActive()
        #
        # Every check below assumes we're in an HA environment.
        elif service.name.startswith("corosync"):
            corosyncInstalled = True
            service.validateEnabledAndActive()
        elif service.name.startswith("pacemaker"):
            pacemakerInstalled = True
            service.validateEnabledAndActive()
        elif service.name.startswith("docker"):
            dockerInstalled = True
            service.validateDisabledAndStopped()
        elif service.name.startswith("serviced"):
            servicedInstalled = True
            service.validateDisabledAndStopped()


    if not dnsmasqInstalled:
        print "The dnsmasq service is not installed"

    if not dockerInstalled:
        print "The docker service is not installed"

    if not ntpInstalled:
        print "The ntp service is not installed"
        print_time_sync_warning()

    if isHA:
        if not corosyncInstalled:
            print "The corosync service is not installed"

        if not pacemakerInstalled:
            print "The pacemaker service is not installed"

if __name__ == "__main__":
    main()
