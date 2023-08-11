if [ $# -ne 3 ]
then
    echo "usage $0 [input] [output-prefix] [column of interest!]"
    exit
fi
cat $1 | grep -v scheme | sed 's/bbr/Scheme-C/g;s/vegas/Scheme-D/g;s/cubic/Scheme-A/g;s/ledbat/Scheme-B/g;' > file

cat > tmp.gpl <<END
load '~/gnuplot-palettes/parula.pal'
set style line 11 lw 2 lt 1 pt 7 lc rgb '#0072bd' # blue
set style line 12 lw 2 lt 1 pt 3 lc rgb '#d95319' # orange
set style line 13 lw 2 lt 1 pt 5 lc rgb '#edb120' # yellow
set style line 14 lw 2 lt 1 pt 9 lc rgb '#7e2f8e' # purple
set style line 15 lw 2 lt 1 pt 4 lc rgb '#77ac30' # green
set style line 16 lw 2 lt 1 lc rgb '#4dbeee' # light-blue
set style line 17 lw 2 lt 1 lc rgb '#a2142f' # red
set terminal svg size 700,262 dynamic enhanced fname 'arial'  fsize 12
set output '$2.svg'
red = "#FF0000"; green = "#00FF00"; blue = "#0000FF"; skyblue = "#87CEEB";
#set yrange [0:50]
set ylabel "Score"
set y2range [0:3]
set ytics nomirror
#set y2tics 0.6 nomirror tc lt 2
#set y2label 'Relative Score (A/B)' tc ls 15
set xlabel "Buffer Size (KB)"
#set offset -1.3,-0.4,0,0
#set offset -.5,-0.4,0,0
set logscale x 2
set xrange [50:*]
#set style data histogram
#set style histogram cluster gap 1
#set style fill solid border -1
#set boxwidth 0.9
#set xtics rotate by -45
#set xtics format ""
#set grid ytics
set key right inside top vertical
#set title "Delay Improvements Normalized to TailDrop"
set key autotitle columnheader
#plot 2*x linetype 1, 4*x linetype 2 axes x1y2

set multiplot layout 1, 2 ;
#set title "Figure 1";
plot "file" using 1:2 with linespoints ls 11, \
    '' using 1:3 with linespoints ls 12
#set title "Figure 1";
set ylabel 'Relative Score (A/B) '
set logscale y 2
set yrange [0.25:4]
plot "file" using 1:4 with linespoints ls 15 title "Relative Scores"
unset multiplot

#plot "file" using 1:4 with linespoints ls 11, \
#   '' using 1:5 with linespoints ls 12, \
#   '' using 1:7 with line ls 15 axes x1y2 notitle
END
gnuplot tmp.gpl 1>tmp

rm tmp* file

