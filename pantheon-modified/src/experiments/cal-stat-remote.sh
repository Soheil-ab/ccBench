if [ $# -ne 3 ]
then
    echo "usage:$0 [folder] [output_file] [avgRTT]"
    exit
fi
../analysis/analyze.py --data-dir $1/

