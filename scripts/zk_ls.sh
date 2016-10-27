#!/bin/bash

# zenoss-inspector-tags serviced zookeeper

# This command will only work on hosts were zookeeper is running

function zk_ls {
    local URL=http://127.0.0.1:12181/exhibitor/v1/explorer/usage-listing?request=%7B%22maxChildrenForTraversal%22%3A1000%2C%22startPath%22%3A%22%2F%22%7D
    local OUTPUT=zk_ls.txt

    wget $URL -O $OUTPUT
}

zk_ls
