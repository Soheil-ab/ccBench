for i in data/dataset-gen-*/tcpdatagen_mm_*.log;
do
    rm $i
done
for i in data/dataset-gen-*/*_mm_*.log;
do
    rm $i
done
for i in data/friendliness-multiflow-all-*/*_mm_*.log
do
    rm $i
done
