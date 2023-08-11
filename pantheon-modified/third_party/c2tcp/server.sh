#!/bin/bash
if [ $# != 4 ]
then
    echo -e "usage:$0 port target period path"
    echo "$@"
    echo "$#"
    exit
fi

port=$1
target=$2
#initial_alpha=$3
period=$3
initial_alpha=150
path=$4

$path/server $port $initial_alpha $target ${period}


