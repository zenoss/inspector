#!/bin/bash

# Make sure unzip is installed
UNZIP_INSTALLED=`rpm -qa unzip`
if [ -z "$UNZIP_INSTALLED" ]; then
	echo "Installing unzip ..."
	yum install -y unzip
fi

# clear out any previous results
rm -rf inspector-gh-temp*

wget -q "https://github.com/zenoss/inspector/archive/master.zip" -O inspector-gh-temp.zip
unzip -qq inspector-gh-temp.zip -d inspector-gh-temp
inspector-gh-temp/inspector-master/inspect
rm -rf inspector-gh-temp*
