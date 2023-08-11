if [ $# -ne 1 ]
then
    echo "usage:$0 scheme"
    exit
fi

cc=$1

data="./data"
pids=""
sys_cpu_cnt=`lscpu | grep "^CPU(s):" | awk '{print $2}'`
cpu_num=$sys_cpu_cnt
cnt=0
period=7

setup_time=10
end_of_ss_comp_segment=3
# We have 4 segments, in single-flow scenario:
# The first segment ([0-3]s) is dedicated for slow-start comparisons &
# 2nd, 3rd, & 4th are dedicated for the "changing" conditions.

for start in 0 3 10 17
do
    for log in $data/dataset-gen*-${cc}-*
    do
        if [ $start -eq 0 ]
        then
            win_end_time=$end_of_ss_comp_segment
        else
            win_end_time=$((start+period))
        fi
        win_start_time=$start
        python ../analysis/save_piecewise.py --data-dir $log --win-start=$((win_start_time+setup_time)) --win-end=$((win_end_time+setup_time)) &
        pids="$pids $!"
        cnt=$((cnt+1))
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

