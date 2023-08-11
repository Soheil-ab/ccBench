schemes="bbr vegas"
pids=""
sys_cpu_cnt=`lscpu | grep "^CPU(s):" | awk '{print $2}'`
cpu_num=$((sys_cpu_cnt/6))
cnt=0
runs=3

for cc in $schemes
do
    for dl in 10 20 30 40 50 60
    do
        qs=$((dl*2*4*5))
        ./cc_solo.sh $cc bench-test 1 $runs 0 $dl $qs "0" 48 30 48 48 5 &
        cnt=$((cnt+1))
        pids="$pids $!"
        sleep 2
        if [ $cnt -gt $cpu_num ]
        then
            for pid in $pids
            do
                wait $pid
            done
            cnt=0
            pids=""
        fi
    done
done

sleep 60
pids=""
for cc in $schemes
do
    for dl in 10 20 30 40 50 60
    do
        qs=$((dl*2*4*5))
        ./cc_solo_analysis.sh $cc bench-test 1 $runs 0 $dl $qs "0" 48 30 48 48 5 &
        pids="$pids $!"
        sleep 1
    done
done
for pid in $pids
do
    wait $pid
done
./rtt_score.sh
