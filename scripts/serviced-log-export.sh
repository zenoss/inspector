#!/bin/bash
# zenoss-inspector-tags slow big servicelogs
# zenoss-inspector-deps serviced-service-list.sh

cleanup ()
{
    # Remove the temp folder
    rm -rf $SLE_TEMP
}

trap cleanup EXIT

# Create a temp folder and an output folder
SLE_TEMP=serviced-log-export-tmp
SLE_OUT=serviced-log-export
mkdir $SLE_TEMP 
mkdir $SLE_OUT 

# Export logs for each top-level service. If we don't specify a top-level service, we will get serviced
#  and other logs that are already pulled by other scripts
awk '/^  [^ ]/{print $2}' serviced-service-list.sh.stdout | while read -r svcid ; do
    tarfile=$SLE_TEMP/$svcid.tgz
    outfolder=$SLE_OUT/$svcid

    serviced log export --service=$svcid --out=$tarfile || continue
    
    # Make the output folder
    mkdir $outfolder || continue
    
    # Extract tgz to the final output dir
    tar -xzf $tarfile -C $outfolder --strip 1 || continue

    # cat the index file and modify it to show relative paths to the files
    echo "SERVICE: $svcid"
    cat $outfolder/index.txt | sed "s;\([0-9][0-9]*.log\);$outfolder/\1;" || continue

done

exit $?


