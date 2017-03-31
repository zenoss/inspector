#!/usr/bin/env python

# zenoss-inspector-info
# zenoss-inspector-tags time-drift verify
# zenoss-inspector-deps time-drift.sh


def main():
    # Open and read standard file
    with open('time-drift.sh.stdout', 'r') as f:
        lines = f.readlines()
    # Open and read error file
    with open('time-drift.sh.stderr', 'r') as g:
        elines = g.readlines()
    # Check for errors
    ehost = 0
    for line in elines:
        if 'no server suitable for synchronization found' in line:
            ehost += 1
            # The name of the host is not recorded during an error
    if ehost > 0:
        print 'WARN: %i host could not be reached for time-drift.' % ehost
    # Check for issues with time-drift
    host = "none"
    hostb = "none"
    checkTime = False
    for line in lines:
        if 'ntpdate -q' in line:
            host = line.split()[-1]
            checkTime = False
            if host == hostb:
                ehost -= 1
                print 'WARN: resource pool member %s could not be reached.' % hostb
            hostb = host
        if 'sec' in line:
            timeshift = float(line.split()[-2])
            checkTime = True
        if checkTime:
            checkTime = False
            # CHECK: 5 second check
            if timeshift > 5.00:
                print "WARN: Time drift too great between the resource pool member:%s with %.3f for the time-drift." % (host, timeshift)
            # if timeshift < 5:
            #     print 'Good: time drift less than 5 seconds for %s' % host        
    # Detect if last resource pool member was reachable
    if host == hostb and ehost > 0:
        print 'WARN: resource pool member: %s, could not be reached.' % hostb

if __name__ == "__main__":
  main()

