if [ $# -ne 11 ]
then
    echo "usage:$0 scheme [kernel based TCPs: vegas bbr reno cubic ...] [log comment] [num of flows] [num of runs] [interval bw flows] [one-way delay] [qs] [down link] [time] [bw] [bw2]"
    exit
fi

scheme=$1
comment=$2
num_of_flows=$3
num_times=$4
interval=$5
delay=$6
qs_=$7
loss_=0
downlink=$8
duration=${9}
bw=${10}
bw2=${11}
trace_period=7
basetimestamp_fld=`pwd -P`
basetimestamp_fld="$basetimestamp_fld\/data"

loss="$loss_"
dl=$downlink
downl="wired$dl"
upl=$downl
lat=$delay
qs=$qs_
time=$duration
down=$downl
log=${comment}-$scheme-$down-$lat-$qs-$loss-$interval
echo "************************ Running $log *********************************"

python2.7 test.friendliness.py local --schemes tcpdatagen --uplink-trace traces/$down --downlink-trace traces/$upl -t $time --extra-mm-link-args \
    "--uplink-queue=droptail --uplink-queue-args=\"packets=$qs\" --downlink-queue=droptail --downlink-queue-args=\"packets=$qs" \
    --prepend-mm-cmds " mm-loss uplink $loss mm-loss downlink $loss mm-delay $lat " \
    --setup_time 2 --orcalearn 4 --random-order -f $num_of_flows --interval $interval --run-times $num_times --data-dir   data/$log   \
    --save 1 --rm 0 --comment \"${num_of_flows}-cubic-added_${down}_${lat}_${qs}_${loss}_${interval}\" --tcpgen_cc $scheme \
    --bw $bw --basetime_fld  "$basetimestamp_fld\/$log\/tcpdatagen_mm_acklink_run1.log_init_timestamp" --bw2 $bw2 --trace_period $trace_period
