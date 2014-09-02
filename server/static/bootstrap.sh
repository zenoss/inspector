INSPECTOR_HOSTNAME="zenpip.zendev.org"
INSPECTOR_PORT="1774"
INSPECTOR_HOST="http://zenpip.zendev.org:1774"

cd /tmp
sudo rm -rf inspector inspector.tar.gz
wget -q $INSPECTOR_HOST"/static/inspector.tar.gz" -O inspector.tar.gz
tar -xzvf inspector.tar.gz
cd inspector
INSPECTOR_HOSTNAME=$INSPECTOR_HOSTNAME INSPECTOR_PORT=$INSPECTOR_PORT ./inspect
