if [ $# -ne 13 ]
then
    echo "usage:$0 scheme [kernel based TCPs: vegas bbr reno cubic ...] [log comment] [num of flows] [num of runs] [interval bw flows] [one-way delay] [qs] [loss] [down link] [time] [bw] [bw2] [setup_time]"
    exit
fi
#source bias.sh
latency=10
scheme=$1
comment=$2
num_of_flows=$3
num_times=$4
interval=$5
lat=$6
qs=$7
loss="$8"
dl=$9
duration=${10}
bw=${11}
bw2=${12}
setup_time=${13}
trace_period=7
basetimestamp_fld=`pwd -P`
basetimestamp_fld="$basetimestamp_fld\/data"

downl="wired$dl"
upl=$downl
bdp=$((2*dl*lat/12))      #12Mbps=1pkt per 1 ms ==> BDP=2*del*BW=2*del*dl/12
time=$duration
down=$downl
log=${comment}-$scheme-$down-$lat-$qs-$loss-$interval
echo "************************running $logfile*********************************"

./cal-stat-remote.sh data/$log $comment-$downl 0
python friendliness-analysis.py --datadir data/$log
