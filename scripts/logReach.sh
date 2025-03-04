#!/bin/bash
#logReach.sh
shopt -s nocasematch
#echo "Please choose an option:"
declare -gA insCount
function appendsCount(){        
        insCount[$1]=$2;
}

function printCounts(){

        for key in "${!insCount[@]}"; do
                echo "$key: ${insCount[$key]}"
        done
}

function getOpts(){
if [ $# -gt 0 ]; then
        #printf "Checking Selected Service:$@\n";
                #for arg in "$@"; do
                #       echo "$arg";
                #done
        service="$@"
    else echo "Service is not set"
        echo 'Please Specify a service';
        read service
fi
serviced service status $service| sed "1 d"|while read lines ; do
        POOLID=$(echo $lines|awk -F'/' '{print $6}'); 
        SVCNT=$(serviced service status $(echo $lines| awk '{print $2}')|grep -c $(echo $lines| awk '{print $1}'));
        echo "$POOLID" "Number of Instances: $SVCNT";
done
}
getOpts $1
echo "--------------------%1%--------------------"
read -p "Specify a Collector Pool: " POOLID
echo "--------------------%2%--------------------"
read -p "Specify the number of instances: " SVCNT
echo "--------------------%3%--------------------"
echo "You have selected to export $service logs from the $POOLID pool"
echo "--------------------%4%--------------------"
echo "Compiling logs"
SVCNT=$((SVCNT-1))
for i in $(seq 0 $SVCNT); do (echo $'\n\n'$service': '$i; serviced service attach $POOLID/$service/$i grep -i "error" /opt/zenoss/log/$service.log | awk '{$1=$2=$3=$4=""; print $0}' | sort -u);
done|& tee /tmp/$service'_failures-'$POOLID.txt && echo "COMPLETED! LOG AVAILABLE AT: /tmp/${service}_failures-$POOLID.txt"  
echo "Download to  your system with 'scp $(hostname):/tmp/${service}_failures-$POOLID.txt ~/Downloads/'"
