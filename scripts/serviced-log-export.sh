#!/bin/bash
# zenoss-inspector-tags slow big servicelogs
# zenoss-inspector-deps serviced-service-list.sh

cleanup ()
{
    echo "cleaning up"
    # Remove the temp folder
    rm -rf $SLE_TEMP
}

trap cleanup EXIT


# Create a temp folder
SLE_TEMP=serviced-log-export-tmp
SLE_OUT=serviced-log-export
mkdir $SLE_TEMP 
mkdir $SLE_OUT 

# Export logs
# TODO: Export for top-level services only.  
#   Otherwise, this includes serviced and other logs that are already pulled by other scripts
serviced log export --out=$SLE_TEMP/out.tgz

# Extract tgz to the final output dir
tar -xzf $SLE_TEMP/out.tgz -C $SLE_OUT --strip 1

# cat the index file and modify it to show relative paths to the files
cat $SLE_OUT/index.txt | sed s/"\([0-9][0-9]*.log\)"/"final\/\1"/

exit $?


