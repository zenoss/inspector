#!/bin/bash

# zenoss-inspector-tags serviced zookeeper

# This command will only work on hosts were zookeeper is running

function zk_ls {
    local OUTPUT=zk_ls.txt
    docker exec serviced-isvcs_zookeeper bash -c \
        '$ZK_PATH/bin/zkCli.sh -server 127.0.0.1:2181 ls -R /' 2>/dev/null | grep '^/' >$OUTPUT
}

zk_ls
