#!/usr/bin/env python

# zenoss-inspector-tags slow big servicelogs
# zenoss-inspector-files

from subprocess import call
import json
import argparse
import os

def main():

    parser = argparse.ArgumentParser()
    parser.add_argument("path")
    args = parser.parse_args()
    
    outFile = os.path.join(args.path, "servicedLogExport.tgz")

    print "Exporting logs to %s" % outFile

    cmd = ["serviced", "log", "export", "--out", outFile]
    call(cmd)

if __name__ == "__main__":
    main()
