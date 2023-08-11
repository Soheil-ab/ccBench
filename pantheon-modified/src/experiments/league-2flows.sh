
#schemes="veno cdg highspeed hybla illinois westwood yeah htcp bic cubic vegas reno bbr2"
#schemes="c2tcp copa sprout ledbat"
#schemes="sage orca dbbr vivace indigo"
schemes="vegas cubic"

output="charts-overall-ranking-multi"

period=30
setup_time=10
data="./data/"
intervals="5"
win_margin=10           # Any scheme perfomring between [(win_margin/100)% of the best, the best] will be considered as a winner.

starts=`seq 0 $period $((120-period))`
for s in $starts
do
    for interval in $intervals
    do
        start=$((s+interval+setup_time))
        end=$((start+period))
        python ../analysis/league-piecewise-2flows.py --datadir $data --win-start=$start --win-end=$end --interval=$interval --prefix=dataset-gen --win-margin=$win_margin --schemes="$schemes"

        for j in $data/dataset-gen-league-multiflows-${start}_${end}
        do
            rm $j/chart*
            num_env=`cat $j/num_env | grep total | awk '{print $2}'`
            for i in $schemes
            do
                cat $j/winners | grep -e "^${i}_2" | awk -v s="$i" -v n_env="$num_env" 'END{print s"\t "NR"\t "NR/n_env}' >>$j/chart
            done

            sort -k2 -rh $j/chart > $j/charts
            rm $j/chart;#echo $j;cat $j/charts
        done
    done
    echo "Done with date/dataset-gen-league-${start}_${end}/winners-dataset/ ...................."
done

declare -A sum
declare -A norm
for i in $schemes
do
    sum[$i]=0
done
for cc in $schemes
do
    for s in $starts
    do
        for interval in $intervals
        do
            start=$((s+interval+setup_time))
            end=$((start+period))
            for i in $data/dataset-gen-league-multiflows-${start}_${end};
            do
                d=`cat $i/charts | awk -v sch="$cc" '{if($1==sch)print $2}'`; sum[$cc]=$((sum[$cc]+d));
            done
        done
    done
done
total=0
for cc in $schemes
do
    total=$((sum[$cc]+total))
done
rm $data/num_env $data/total $data/total_l $data/total_nl

for i in $data/dataset-gen-league-multi*;
do
    cat $i/num_env
    echo "`cat $i/num_env | grep total | awk '{print $2}'`" >> $data/total
done

total=`cat $data/total | awk 'BEGIN{s=0}{s=s+$1}END{print s}'`

for cc in $schemes
do
    norm[$cc]=`printf %.2f "$((1000000000  *  100*sum[$cc]/total))e-9"`
done
rm tmp tmp2
for cc in $schemes
do
    echo "$cc ${sum[$cc]} ${norm[$cc]} $total" >> tmp
done
sort -k2 -hr tmp > tmp2
column -t tmp2 > tmp

rm $data/${output}
echo -e "scheme wins % num_games" >> $data/${output}

cat tmp >> $data/${output}
cat $data/${output}
rm tmp*

