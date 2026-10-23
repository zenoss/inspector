#!/bin/bash
# zenoss-inspector-tags serviced zookeeper docker
# zenoss-inspector-deps ps-aux.sh
# Needs Docker running (per ps-aux.sh.stdout) and serviced-isvcs_zookeeper.
# zk_ls.txt lists every znode path. zk_counts.txt has "<path> <count>" for /
# and each top-level znode (from its own "ls /"), counting all znodes below it.
# zkCli connects to 127.0.0.1:${ZK_CLIENT_PORT:-2181} inside the container.
# If serviced uses ZooKeeper digest ACLs (SERVICED_ZOOKEEPER_ACL_USER and
# SERVICED_ZOOKEEPER_ACL_PASSWD, from the environment or else from
# ${SERVICED_DEFAULTS:-/etc/default/serviced}), each zkCli session first runs
# "addauth digest" with them; the password goes to zkCli on stdin only.
# Any failure (container missing, ZooKeeper down, zkCli error such as NoAuth,
# count mismatch, credentials with whitespace or a user starting with '-')
# exits non-zero; details are in zk_ls.err. Each step writes <name>.partial and
# renames it to <name> only on success; zk_counts runs even if zk_ls failed.
set -o pipefail
ERRORS=zk_ls.err
# zkCli errors on stderr. zkCli's exit status is that of its last command, so
# an earlier failed command in a session can still exit 0.
ZK_ERROR='Insufficient permission|KeeperErrorCode|NoAuth|AuthFailed|Node does not exist|Command not found|Exception|ERROR'

# Prints the value of the last uncommented "<name>=<value>" in the serviced
# defaults file, with one pair of surrounding quotes removed. Parsed, not sourced.
function defaults_value {
    local line value=
    local file=${SERVICED_DEFAULTS:-/etc/default/serviced}
    [ -r "$file" ] || return 0
    while IFS= read -r line || [ -n "$line" ]; do
        line=${line%$'\r'}
        line=${line#"${line%%[![:space:]]*}"}
        case $line in
        export[[:space:]]*)
            line=${line#export}
            line=${line#"${line%%[![:space:]]*}"}
            ;;
        esac
        case $line in "$1="*) value=${line#"$1="} ;; esac
    done <"$file"
    case $value in
    \"*\" | \'*\') value=${value:1:${#value}-2} ;;
    esac
    printf '%s' "$value"
}

if [ -n "${SERVICED_ZOOKEEPER_ACL_USER+set}" ] && [ -n "${SERVICED_ZOOKEEPER_ACL_PASSWD+set}" ]; then
    ACL_USER=$SERVICED_ZOOKEEPER_ACL_USER
    ACL_PASSWD=$SERVICED_ZOOKEEPER_ACL_PASSWD
else
    ACL_USER=$(defaults_value SERVICED_ZOOKEEPER_ACL_USER)
    ACL_PASSWD=$(defaults_value SERVICED_ZOOKEEPER_ACL_PASSWD)
fi

# First line of every zkCli session's stdin: authenticate when both are set.
# printf is a builtin, so the password is never on a command line.
function zk_auth {
    if [ -n "$ACL_USER" ] && [ -n "$ACL_PASSWD" ]; then
        printf 'addauth digest %s:%s\n' "$ACL_USER" "$ACL_PASSWD"
    fi
}

# Appends a zkCli session's stderr ($1) to zk_ls.err; fails if the session's
# exit status ($2) is non-zero or its stderr reports an error.
function zk_check {
    local stderr=$1 status=$2 name=$3
    cat "$stderr" >>$ERRORS
    if [ "$status" -ne 0 ]; then
        echo "$name: docker exec/zkCli exited $status" >>$ERRORS
        return 1
    fi
    if grep -qE "$ZK_ERROR" "$stderr"; then
        echo "$name: zkCli reported an error" >>$ERRORS
        return 1
    fi
}

function zk_ls {
    local OUTPUT=zk_ls.txt.partial
    local status
    { zk_auth; echo 'ls -R /'; } |
        docker exec -i serviced-isvcs_zookeeper bash -c \
            '$ZK_PATH/bin/zkCli.sh -server 127.0.0.1:${ZK_CLIENT_PORT:-2181}' 2>"$TMP_ERR" |
        sed -E 's/^(\[zk: [^]]*\] *)+//' | grep '^/' >$OUTPUT
    status=("${PIPESTATUS[@]}")
    zk_check "$TMP_ERR" "${status[1]}" zk_ls || return 1
    if [ "${status[3]}" -ne 0 ]; then
        echo "zk_ls: no znode paths in zkCli output" >>$ERRORS
        return 1
    fi
    mv -f $OUTPUT zk_ls.txt
}

function zk_counts {
    local OUTPUT=zk_counts.txt.partial
    local paths status
    # zkCli prints "ls /" as one "[a, b, zookeeper]" line. Paths come from this
    # session, not zk_ls.txt, so the counts do not depend on zk_ls's output.
    { zk_auth; echo 'ls /'; } |
        docker exec -i serviced-isvcs_zookeeper bash -c \
            '$ZK_PATH/bin/zkCli.sh -server 127.0.0.1:${ZK_CLIENT_PORT:-2181}' 2>"$TMP_ERR" |
        sed -E 's/^(\[zk: [^]]*\] *)+//' |
        awk '/^\[.*\]$/ {lists++; gsub(/^\[|\]$/, ""); n = split($0, name, ", ")}
            END {if (lists != 1 || n == 0) exit 1; print "/"; for (i = 1; i <= n; i++) print "/" name[i]}' >"$TMP_PATHS"
    status=("${PIPESTATUS[@]}")
    zk_check "$TMP_ERR" "${status[1]}" zk_counts || return 1
    if [ "${status[3]}" -ne 0 ]; then
        echo "zk_counts: no top-level paths from zkCli ls /" >>$ERRORS
        return 1
    fi
    paths=$(<"$TMP_PATHS")
    # One zkCli session runs the commands from stdin and prints each count
    # after its prompt(s), in order, without naming the path; pair them by order.
    { zk_auth; sed 's/^/getAllChildrenNumber /' <<<"$paths"; } |
        docker exec -i serviced-isvcs_zookeeper bash -c \
            '$ZK_PATH/bin/zkCli.sh -server 127.0.0.1:${ZK_CLIENT_PORT:-2181}' 2>"$TMP_ERR" |
        awk 'NR == FNR {path[++n] = $0; next}
            {sub(/^(\[zk: [^]]*\] *)+/, "")}
            /^[0-9]+$/ {count[++m] = $0}
            END {if (m != n) exit 1; for (i = 1; i <= n; i++) print path[i], count[i]}' \
            <(echo "$paths") - >$OUTPUT
    status=("${PIPESTATUS[@]}")
    zk_check "$TMP_ERR" "${status[1]}" zk_counts || return 1
    if [ "${status[2]}" -ne 0 ]; then
        echo "zk_counts: got a different number of counts than paths" >>$ERRORS
        return 1
    fi
    mv -f $OUTPUT zk_counts.txt
}

# zkCli splits its input on whitespace and parses a leading '-' as an option,
# so such credentials cannot be passed intact; refuse them, naming neither.
function zk_creds_ok {
    [ -n "$ACL_USER" ] && [ -n "$ACL_PASSWD" ] || return 0
    case $ACL_USER in *[[:space:]]* | -*) return 1 ;; esac
    case $ACL_PASSWD in *[[:space:]]*) return 1 ;; esac
}

function failed {
    echo "$1 failed; see zk_ls.err" >&2
}

: >$ERRORS
rm -f zk_ls.txt zk_counts.txt zk_ls.txt.partial zk_counts.txt.partial
# The same check as docker-stats.sh, before any docker call.
egrep "(docker -d|docker daemon|dockerd)" ps-aux.sh.stdout &>/dev/null
if [ $? -ne 0 ]; then
    echo "Docker doesn't appear to be running." | tee -a $ERRORS >&2
    exit 1
fi
TMP_ERR=$(mktemp) && TMP_PATHS=$(mktemp) || exit 1
trap 'rm -f "$TMP_ERR" "$TMP_PATHS"' EXIT
DEFAULTS=${SERVICED_DEFAULTS:-/etc/default/serviced}
[ -e "$DEFAULTS" ] && [ ! -r "$DEFAULTS" ] && echo "zk_ls: cannot read $DEFAULTS; ACL credentials not loaded from it" >>$ERRORS
if ! zk_creds_ok; then
    echo "zk_ls: ACL credentials contain whitespace or start with '-'; zkCli cannot pass them" >>$ERRORS
    failed zk_ls
    exit 1
fi
RC=0
zk_ls || { failed zk_ls; RC=1; }
zk_counts || { failed zk_counts; RC=1; }
exit $RC
