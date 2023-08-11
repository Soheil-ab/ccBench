schemes="ledbat cubic"
runs=3
pids=""
sys_cpu_cnt=`lscpu | grep "^CPU(s):" | awk '{print $2}'`
cpu_num=$((sys_cpu_cnt/6))
cnt=0

for cc in $schemes
do
    for qs in 40 80 160 320 640
    do
        ./cc_solo.sh $cc bench-test 1 $runs 0 20 $qs "0" 48 30 48 48 5 & sleep 2
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

for cc in $schemes
do
    for qs in 40 80 160 320 640
    do
        ./cc_solo_analysis.sh $cc bench-test 1 $runs 0 20 $qs "0" 48 30 48 48 5 &
        pids="$pids $!"
    done
done
for pid in $pids
do
    wait $pid
done
./buffersize_score.sh
