#!/bin/bash
# zenoss-inspector-tags serviced zookeeper
# Needs the docker CLI and a running serviced-isvcs_zookeeper container.
# zk_ls.txt lists every znode path. zk_counts.txt has "<path> <count>" for /
# and each top-level znode, where count is all znodes below it.
function zk_ls {
    local OUTPUT=zk_ls.txt
    set -o pipefail
    docker exec serviced-isvcs_zookeeper bash -c \
        '$ZK_PATH/bin/zkCli.sh -server 127.0.0.1:2181 ls -R /' 2>zk_ls.err | grep '^/' >$OUTPUT ||
        echo "zk_ls failed; see zk_ls.err" >&2
}
function zk_counts {
    local OUTPUT=zk_counts.txt
    local paths
    [ -s zk_ls.txt ] || return 0
    paths=$(awk 'NR == 1 {print "/"} /^\/[^\/]+$/' zk_ls.txt)
    # One zkCli session runs the commands from stdin and prints each count
    # after its prompt, in order, without naming the path; pair them by order.
    sed 's/^/getAllChildrenNumber /' <<<"$paths" |
        docker exec -i serviced-isvcs_zookeeper bash -c \
            '$ZK_PATH/bin/zkCli.sh -server 127.0.0.1:2181' 2>>zk_ls.err |
        awk 'NR == FNR {path[++n] = $0; next}
            {sub(/^\[zk: [^]]*\] */, "")}
            /^[0-9]+$/ {count[++m] = $0}
            END {if (m != n) exit 1; for (i = 1; i <= n; i++) print path[i], count[i]}' \
            <(echo "$paths") - >$OUTPUT ||
        echo "zk_counts failed; see zk_ls.err" >&2
}
zk_ls
zk_counts
