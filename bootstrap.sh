rm -rf inspector-gh-temp*
wget -q "https://github.com/zenoss/inspector/archive/master.zip" -O inspector-gh-temp.zip
unzip -qq inspector-gh-temp.zip -d inspector-gh-temp
inspector-gh-temp/inspector-master/inspect
rm -rf inspector-gh-temp*
