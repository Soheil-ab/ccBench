if [ $# -ne 13 ]
then
    echo "usage:$0 scheme [kernel based TCPs: vegas bbr reno cubic ...] [log comment] [num of flows] [num of runs] [interval bw flows] [one-way delay] [qs] [loss] [down link] [time] [bw] [bw2] [setup_time]"
    exit
fi
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
echo "************************ Running $log*********************************"

python2.7 test.friendliness.py local --schemes $scheme --uplink-trace traces/$down --downlink-trace traces/$upl -t $time \
    --extra-mm-link-args "--uplink-queue=droptail --uplink-queue-args=\"packets=$qs\" --downlink-queue=droptail --downlink-queue-args=\"packets=$qs" \
    --prepend-mm-cmds " mm-loss uplink $loss mm-loss downlink $loss mm-delay $lat " \
    --setup_time $setup_time --orcalearn 4 --random-order -f $num_of_flows --interval $interval --run-times $num_times --data-dir   data/$log   \
    --save 1 --rm 0 --comment \"${num_of_flows}-cubic-added_${down}_${lat}_${qs}_${loss}_${interval}\" --tcpgen_cc $scheme --bw $bw \
    --basetime_fld  "$basetimestamp_fld\/$log\/tcpdatagen_mm_acklink_run1.log_init_timestamp" --bw2 $bw2 --trace_period $trace_period --srate "24M"
