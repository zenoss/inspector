cd /tmp
sudo rm -rf inspector inspector.tar.gz
wget -q "http://{{hostname}}:{{port}}/static/inspector.tar.gz" -O inspector.tar.gz
tar -xzvf inspector.tar.gz
cd inspector
INSPECTOR_HOSTNAME="{{hostname}}" INSPECTOR_PORT="{{port}}" sudo ./inspect
