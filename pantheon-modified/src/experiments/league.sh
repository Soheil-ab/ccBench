
period=7
#schemes="veno cdg highspeed hybla illinois westwood yeah htcp bic cubic bbr2 vegas reno"
#schemes="$schemes indigo vivace aurora orca dbbr"
#schemes="$schemes pure"
#schemes="$schemes $1 $2"

#A sample:
schemes="vegas cubic"

output="charts-overall-ranking-single-flow"

data="./data"
win_margin=10 # % -> 10: 10% ==> everyone in the range of [0.9*best,best] is a winner.

end_of_ss_comp_segment=3

for start in 0 3 10 17
do
    if [ $start -eq 0 ]
    then
        #Slow-Start:
        end=$end_of_ss_comp_segment
    else
        #Other Segments:
        end=$((start+period))
    fi
    for j in $data/dataset-gen-league-*
    do
        rm -r $j/log
    done

    python ../analysis/league-piecewise.py --datadir $data/ --win-start=$((start+setup_time)) --win-end=$((end+setup_time)) --win-margin=$win_margin --schemes="$schemes"

    for j in $data/dataset-gen-league-*
    do
        rm $j/chart $j/charts
        num_env=`cat $j/num_env | grep total | awk '{print $2}'`
        for i in $schemes
        do
            cat $j/winners | grep -e "^${i}_" | awk -v s="$i"  -v n_env="$num_env" 'END{print s"\t "NR"\t "NR/n_env}' >>$j/chart
        done
        sort -k2 -rh $j/chart > $j/charts
        echo $j;cat $j/charts
    done
    echo " ---------------- Done with date/dataset-gen-league-${start}_${end}/winners-dataset/ ------------------"
done

#COMMENT
declare -A sum
declare -A norm
for i in $schemes
do
    sum[$i]=0;
done
for cc in $schemes
do
    for i in $data/dataset-gen-league-*;
    do
        d=`cat $i/charts | awk -v sch="$cc" '{if($1==sch)print $2}'`;    sum[$cc]=$((sum[$cc]+d));
    done
done

total=0
for cc in $schemes
do
    total=$((sum[$cc]+total));
done
rm $data/num_env $data/total

for i in $data/dataset-gen-league-*;
do
    cat $i/num_env
    echo "`cat $i/num_env | grep total | awk '{print $2}'`" >> $data/total
done

total=`cat $data/total | awk 'BEGIN{s=0}{s=s+$1}END{print s}'`

for cc in $schemes
do
    norm[$cc]=`printf %.2f "$((1000000000  *  100*sum[$cc]/total))e-9"`
done

rm tmp tmp2 tmp_l tmp_l2 tmp_nl tmp_nl2
for cc in $schemes
do
    echo "$cc ${sum[$cc]} ${norm[$cc]} $total" >> tmp
done
sort -k2 -hr tmp > tmp2;
column -t tmp2 > tmp;

rm $data/${output}-$win_margin

echo -e "scheme wins % num_games" >> $data/${output}-$win_margin

cat tmp >> $data/${output}-$win_margin
cat $data/${output}-$win_margin
rm tmp*
