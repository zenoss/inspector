#!/usr/bin/env python                                                                                                                                       

# zenoss-inspector-info                                                                                                                                     
# zenoss-inspector-tags os verify                                                                                                                           
# zenoss-inspector-deps serviced-storage.sh storage-config.sh                                                                                               
import re

def main():
    with open("serviced-storage.sh.stdout", 'r') as f1:
        for line1 in f1.readlines():
            if "Application Data" in line1:
                volId = line1.split()[0]
                path = "/opt/serviced/var/volumes/.devicemapper/volumes/" + volId + "/metadata.json"
                with open(path, 'r') as f2:
                    line2 = f2.readline()
                    pattern1 = re.compile('^\{\"CurrentDevice\"\:\"(?P<blkId>\w*)')
                    pool = pattern1.match(line2).group('blkId')

                with open("storage-config.sh.stdout", 'r') as f3:
                    for line3 in f3.readlines():
                        line3 = ''.join(i for i in line3 if ord(i)<128)
                        if "lv-display" in line3:
                            return
                        if "/exports/serviced_volumes_v2/" in line3:
                            pattern2 = re.compile('.*:\d+(-\d+)-(?P<poolId>\w*)\s.*')
                            upool = pattern2.match(line3).group('poolId')
                            if upool != pool:
                                print "Storage volume mismatch on serviced-serviced--pool: %s see lsblk output, for more information see defect CC-2487" % pool
                                print "If you have Zenoss Enterprise Support availble it is suggested to open a support case for further assistance. For Zenoss Community users please reference KB article (TBD)."
if __name__ == "__main__":
    main()
