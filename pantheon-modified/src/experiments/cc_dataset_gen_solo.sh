if [ $# -ne 12 ]
then
    echo "usage:$0 scheme [kernel based TCPs: vegas bbr reno cubic ...] [log comment] [num of flows] [num of runs] [interval bw flows] [one-way delay] [qs] [loss] [down link] [duration] [BW (Mbps)] [BW2 (Mbps)]"
    exit
fi
sudo sysctl -w net.ipv4.ip_forward=1
latency=10
scheme=$1
comment=$2
num_of_flows=$3
num_times=$4
interval=$5
delay=$6
qs_=$7
loss_=$8
downlink=$9
duration=${10}
bw=${11}
bw2=${12}
trace_period=7
setup_time=2

basetimestamp_fld=`pwd -P`
basetimestamp_fld="$basetimestamp_fld\/data"

loss="$loss_"
dl=$downlink
downl="wired${dl}"
upl=$downl
lat=$delay
qs=$qs_
time=$duration
down=$downl
log=${comment}-$scheme-$down-$lat-$qs-$loss
echo "************************ Running $log *********************************"

python2.7 test.py local --schemes tcpdatagen --uplink-trace traces/$down --downlink-trace traces/$upl -t $time \
--extra-mm-link-args "--uplink-queue=droptail --uplink-queue-args=\"packets=$qs\" --downlink-queue=droptail --downlink-queue-args=\"packets=$qs" \
--prepend-mm-cmds " mm-loss uplink $loss mm-loss downlink $loss mm-delay $lat " \
--setup_time $setup_time --orcalearn 4 --random-order -f $num_of_flows --interval $interval --run-times $num_times --data-dir data/$log  \
--save 1 --rm 0 --comment \"${down}_${lat}_${qs}_${loss}\" --tcpgen_cc $scheme --bw $bw \
--basetime_fld "$basetimestamp_fld\/$log\/tcpdatagen_mm_acklink_run1.log_init_timestamp" --bw2 $bw2 --trace_period $trace_period
