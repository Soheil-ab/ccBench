time=120
setup_time=10
./system_setup.sh
pids=""
sys_cpu_cnt=`lscpu | grep "^CPU(s):" | awk '{print $2}'`
cnt=0
loss_list="0"
bw_list="12 24 48 96 192"
del_list="5 10 20 40 80"
interval_list="5"

#schemes="pure orca c2tcp dbbr"
#A sample
schemes="vegas cubic"

for cc in $schemes
do
    for loss in $loss_list
    do
        for bw in $bw_list
        do
            if [ $bw -gt 100 ]
            then
                cpu_num=$((sys_cpu_cnt/16))
            else
                cpu_num=$((sys_cpu_cnt/12))
            fi
            for del in $del_list
            do
                bdp=$((del*bw/6))
                for qs in $bdp $((2*bdp)) $((4*bdp)) $((8*bdp)) $((16*bdp))
                do
                    for dl_post in ""
                    do
                        link="$bw$dl_post"
                        for interval in $interval_list
                        do
                            ./cc_multi.sh $cc dataset-gen-1-cubic-added 2 1 $interval $del $qs "$loss" $link $time $bw $bw $setup_time &
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
                            sleep 2
                        done
                    done
                done
            done
            sleep $((time+10))
            sudo killall -s9 iperf iperf3
        done
    done
    #clean tmp folder: all files created before 20min ago will be deleted ...
    ./clean-tmp.sh
done
cpu_num=$((sys_cpu_cnt))
sleep $((time+10))

for cc in $schemes
do
    for loss in $loss_list
    do
        for bw in $bw_list
        do
            for del in $del_list
            do
                bdp=$((del*bw/6))
                for qs in $bdp $((2*bdp)) $((4*bdp)) $((8*bdp)) $((16*bdp))
                do
                    for dl_post in ""
                    do
                        link="$bw$dl_post"
                        for interval in $interval_list
                        do
                            ./cc_multi_analysis.sh $cc dataset-gen-1-cubic-added 2 1 $interval $del $qs "$loss" $link $time $bw $bw $setup_time &
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
        done
    done
done
#clean tmp folder: all files created before 20min ago will be deleted ...
./clean-tmp.sh
for cc in $schemes
do
    ./prepare-multi_league.sh $cc
done


