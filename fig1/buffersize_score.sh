
ccs="cubic ledbat"
declare -A score;
for i in 640 320 160 80 40;
do
    row="$((i*15/10)) ";
    for cc in $ccs
    do
        score[$cc]=`cat data/bench-test-${cc}-wired48-20-$i-0/perf*abs* | grep $cc | awk '{print $2*$2/($3+20)}'`
        row="$row ${score[$cc]}";
    done;
    echo $row >> tmp
done;
echo "buffersize $ccs A/B" > data/buffersize_results
cat tmp
cat tmp | awk '{print $0" "$2/$3}' | sed "s/-nan//g" | column -t > tmp2
cat tmp2 >> data/buffersize_results
./plot.score.buffer.sh data/buffersize_results score_buffer_v3 2
cat data/buffersize_results
