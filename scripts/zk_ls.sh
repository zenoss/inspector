#!/bin/bash
# zenoss-inspector-tags serviced zookeeper
# This command will only work on hosts where zookeeper is running
function zk_ls {
    local OUTPUT=zk_ls.txt
    set -o pipefail
    docker exec serviced-isvcs_zookeeper bash -c \
        '$ZK_PATH/bin/zkCli.sh -server 127.0.0.1:2181 ls -R /' 2>zk_ls.err | grep '^/' >$OUTPUT ||
        echo "zk_ls failed; see zk_ls.err" >&2
}
zk_ls
