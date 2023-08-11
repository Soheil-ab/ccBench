
time=30
timeout=300
./system_setup.sh
pids=""
sys_cpu_cnt=`lscpu | grep "^CPU(s):" | awk '{print $2}'`
cnt=0

#schemes="c2tcp copa vivace ledbat sprout"
#schemes="sage orca indigo dbbr"
schemes="vegas cubic"
setup_time=10

loss_list="0"
bw_list="12 24 48 96 192"
del_list="5 10 20 40 80"

for cc in $schemes
do
    for loss in $loss_list
    do
        ## Pantheon and Mahimahi have problem with links higher than 300Mbps!
        ## For now, avoid using any link BW>300Mbps. But, stay tuned! A new patch is on the way! ;)
        for bw in $bw_list
        do
            if [ $bw -gt 100 ]
            then
                cpu_num=$((sys_cpu_cnt/12))
            else
                cpu_num=$((sys_cpu_cnt/6))
            fi
            for del in $del_list
            do
                bdp=$((del*bw/6))
                for qs in $((bdp/2)) $bdp $((2*bdp)) $((4*bdp)) $((8*bdp)) $((16*bdp))
                do
                    for dl_post in ""
                    do
                        link="$bw$dl_post"
                        echo "./cc_solo.sh $cc dataset-gen 1 1 0 $del $qs "$loss" $link $time $bw $bw $setup_time"
                        ./cc_solo.sh $cc dataset-gen 1 1 0 $del $qs "$loss" $link $time $bw $bw $setup_time &
                        cnt=$((cnt+1))
                        pids="$pids $!"
                        sleep 2
                    done

                    if [ $bw -lt 50 ]
                    then
                        scales="2 4"
                    elif [ $bw -lt 100 ]
                    then
                        scales="2 4"
                    elif [ $bw -lt 200 ]
                    then
                        scales=""
                    else
                        scales=""
                    fi
                    for scale in $scales
                    do
                        dl_post="-${scale}x-u-7s-plus-10"
                        bw2=$((bw*scale))
                        link="$bw$dl_post"
                        echo "./cc_solo.sh $cc dataset-gen 1 1 0 $del $qs "$loss" $link $time $bw $bw2 $setup_time"
                        ./cc_solo.sh $cc dataset-gen 1 1 0 $del $qs "$loss" $link $time $bw $bw2 $setup_time &
                        cnt=$((cnt+1))
                        pids="$pids $!"
                        sleep 2
                    done
                    scales="2 4"
                    for scale in $scales
                    do
                        dl_post="-${scale}x-d-7s-plus-10"
                        bw2=$((bw/scale))
                        link="$bw$dl_post"
                        echo "./cc_solo.sh $cc dataset-gen 1 1 0 $del $qs "$loss" $link $time $bw $bw2 $setup_time &"
                        ./cc_solo.sh $cc dataset-gen 1 1 0 $del $qs "$loss" $link $time $bw $bw2 $setup_time &
                        cnt=$((cnt+1))
                        pids="$pids $!"
                        sleep 2
                    done
                    if [ $cnt -gt $cpu_num ]
                    then
                        for pid in $pids
                        do
                            wait $pid
                        done
                        cnt=0
                        pids=""
                        ./clean-tmp.sh
                    fi
                done
            done
        done
    done
done
sleep 30
cpu_num=$((sys_cpu_cnt))

for cc in $schemes
do
    for loss in $loss_list
    do
        for bw in $bw_list
        do
            for del in $del_list
            do
                bdp=$((del*bw/6))
                for qs in $((bdp/2)) $bdp $((2*bdp)) $((4*bdp)) $((8*bdp)) $((16*bdp))
                do
                    for dl_post in ""
                    do
                        link="$bw$dl_post"
                        echo "./cc_solo_analysis.sh $cc dataset-gen 1 1 0 $del $qs "$loss" $link $time $bw $bw $setup_time"
                        ./cc_solo_analysis.sh $cc dataset-gen 1 1 0 $del $qs "$loss" $link $time $bw $bw $setup_time &
                        cnt=$((cnt+1))
                        pids="$pids $!"
                        sleep 2
                    done
                    if [ $bw -lt 50 ]
                    then
                        scales="2 4"
                    elif [ $bw -lt 100 ]
                    then
                        scales="2 4"
                    elif [ $bw -lt 200 ]
                    then
                        scales=""
                    else
                        scales=""
                    fi
                    for scale in $scales
                    do
                        dl_post="-${scale}x-u-7s-plus-10"
                        bw2=$((bw*scale))
                        link="$bw$dl_post"
                        echo "./cc_solo_analysis.sh $cc dataset-gen 1 1 0 $del $qs "$loss" $link $time $bw $bw2 $setup_time"
                        ./cc_solo_analysis.sh $cc dataset-gen 1 1 0 $del $qs "$loss" $link $time $bw $bw2 $setup_time &
                        cnt=$((cnt+1))
                        pids="$pids $!"
                    done
                    scales="2 4"
                    for scale in $scales
                    do
                        dl_post="-${scale}x-d-7s-plus-10"
                        bw2=$((bw/scale))
                        link="$bw$dl_post"
                        echo "./cc_solo_analysis.sh $cc dataset-gen 1 1 0 $del $qs "$loss" $link $time $bw $bw2 $setup_time"
                        ./cc_solo_analysis.sh $cc dataset-gen 1 1 0 $del $qs "$loss" $link $time $bw $bw2 $setup_time &
                        cnt=$((cnt+1))
                        pids="$pids $!"
                    done
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
./clean-tmp.sh
for cc in $schemes
do
    ./prepare-solo_league.sh $cc
done
./clean-tmp2.sh
