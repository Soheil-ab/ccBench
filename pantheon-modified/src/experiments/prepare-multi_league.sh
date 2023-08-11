if [ $# -ne 1 ]
then
    echo "usage:$0 scheme"
    exit
fi
#schemes="veno cdg highspeed hybla illinois westwood yeah htcp bic cubic vegas reno copa vivace c2tcp bbr2"
#schemes="sage c2tcp copa vivace indigo orca dbbr"
schemes=$1

data="./data"

pids=""
cnt=0
setup_time=10
sys_cpu_cnt=`lscpu | grep "^CPU(s):" | awk '{print $2}'`
cpu_num=$((sys_cpu_cnt))

for period in 30 120
do
    for s in `seq 0 $period 119 `
    do
        for interval in 5
        do
            start=$((s+interval+setup_time))
            end=$((start+period))
            cc=$schemes

            for log in $data/dataset-gen*-added-${cc}-*$interval
            do
                python ../analysis/save_piecewise.py --data-dir $log --win-start=${start} --win-end=${end} &
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
    done
done

