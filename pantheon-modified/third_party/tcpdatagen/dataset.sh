#!/bin/bash

if [ $# != 13 ]
then
    echo -e "usage:$0 port target initial_alpha period first_time [underlying scheme:cubic , vegas , westwood , illinois , bbr, yeah , veno, scal , htcp , cdg , hybla ,... ] [path to ddpg.py] [comment] [number of fows] [BW (Mbps)] [basetimestamp's folder ] [bw2] [trace_period]"
    echo "$@"
    echo "$#"
    exit
fi

port=$1
target=$2
initial_alpha=$3
period=$4
first_time=$5
x=100
scheme=$6
path=$7
comm=$8
num_flows=$9
env_bw=${10}
basetimestamp_fld=${11}
bw2=${12}
trace_period=${13}
tid=0
save=0 # no effect during dataset generation
dl="empty"
up="empty"
del=10
log=${comm}
time=100000
loss=0
qs=100
time_training_steps=0

$path/sage_dataset $port $path $save $num_flows $env_bw 1 $scheme $tid $dl $up $del $log $time $loss $qs $time_training_steps $basetimestamp_fld $bw2 $trace_period


