ccs="vegas bbr"
declare -A score;
for i in 10 20 30 40 50 60;
do
    row="$((i*2))ms ";
    for cc in $ccs;
    do
        score[$cc]=`cat data/bench-test-${cc}-wired48-$i-$((i*40))-0/perf*abs* | grep $cc | awk -v rtt="$i" '{print $2*$2/($3+rtt)}'`;
        row="$row ${score[$cc]}";
    done;
    echo $row >> tmp;
done;
echo "minRTT $ccs C/D " > data/rtt_results
cat tmp | awk '{print $0" "$2/$3}' | sed "s/-nan//g" | column -t > tmp2
cat tmp2 >> data/rtt_results
./plot.score.rtt.sh data/rtt_results score_mrtt_v3 2
cat data/rtt_results
