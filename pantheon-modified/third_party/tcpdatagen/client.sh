#!/bin/bash

if [ $# != 4 ]
then
    echo "usage:$0 ip fid port path"
    echo "$@"
    echo "$#"
exit
fi
#sleep 2
$4/client $1 $2 $3
