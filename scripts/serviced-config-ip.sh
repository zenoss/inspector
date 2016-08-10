#!/bin/bash

# zenoss-inspector-info
# zenoss-inspector-tags serviced config verify
# zenoss-inspector-deps serviced-config.sh

# For any setting that has a hostname set, it should be an IP

settings_with_address=( "SERVICED_ZK" "SERVICED_DOCKER_REGISTRY" "SERVICED_ENDPOINT" "SERVICED_LOG_ADDRESS" "SERVICED_LOGSTASH_ES" "SERVICED_STATS_PORT" )

for setting in "${settings_with_address[@]}"
do
    grep -E -i "$setting=(\{\{SERVICED_MASTER_IP\}\}|[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3})" serviced-config.sh.stdout &> /dev/null

    if [ $? -ne 0 ]
        then
            echo "Your setting for $setting appears to be a hostname. It is recommended to use an IP address for this setting."
        fi
done
