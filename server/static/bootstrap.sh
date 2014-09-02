INSPECTOR_HOSTNAME="localhost"
INSPECTOR_PORT="8080" # Set this to -1 for no port.
INSPECTOR_HOST="http://localhost:8080"

cd /tmp
sudo rm -rf inspector inspector.tar.gz
wget -q $INSPECTOR_HOST"/static/inspector.tar.gz" -O inspector.tar.gz
tar -xzvf inspector.tar.gz
cd inspector
INSPECTOR_HOSTNAME=$INSPECTOR_HOSTNAME INSPECTOR_PORT=$INSPECTOR_PORT ./inspect
