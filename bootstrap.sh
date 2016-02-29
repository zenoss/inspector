#!/bin/bash

# clear out any previous results
rm -rf inspector-gh-temp*

mkdir inspector-gh-temp

curl -s "https://codeload.github.com/zenoss/inspector/tar.gz/master" -o inspector-gh-temp.tar.gz

tar -xf inspector-gh-temp.tar.gz -C inspector-gh-temp

inspector-gh-temp/inspector-master/inspect

rm -rf inspector-gh-temp*
