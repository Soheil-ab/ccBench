if [ $# -ne 3 ]
then
    echo "usage $0 [input] [output-prefix] [column of interest!]"
    exit
fi
cat $1 | grep -v scheme | sed 's/indigo2f/indigov2/g;s/dbbr/DeepCC/g;s/bbr/BBR/g;s/cdg/CDG/g;s/^bic/BIC/g;s/tcp/TCP/g;s/Tcp/TCP/g;s/\([a-z]\)\([a-z]*\)/\U\1\L\2/g;' > file1
sed -i 's/Sage-Online/OnlineRL/g;s/Sagebc/BC/g;s/Pure/Sage/g;s/Ledbat/LEDBAT/g;s/DEep/Deep/g;s/Yeah/YeAH/g;s/Reno/NewReno/g;s/BCtop/BC-top/g;s/BCwinners/BCv2/g' file1
cat file1 | grep Sage > file_sage

#Orange blue v2 : ff9900  vs. #146eb4
cat file1 | awk '{if($1=="Sage" || $1=="Sagebeta") print $0" 0xff9900";else print $0" 0x146eb4" }' > file

#sed -i "s/Sage/Sage\(1-Week\)/g" file
cat > tmp.gpl <<END
#set terminal svg size 350,550 dynamic enhanced fname 'arial'  fsize 14
##### To make it not have a transparent background, uncomment following rectangle!
#set object 1 rectangle \
#    from screen 0,0 to screen 1,1 fillcolor rgb"#FFFFFF" behind
#set terminal svg size 550,250 dynamic enhanced font 'arial,14'

#set terminal svg size 550,700 dynamic enhanced font 'arial,19'
#set terminal svg size 550,350 dynamic enhanced font 'arial,15'
set terminal svg size 450,400 dynamic enhanced font 'arial,15'
set lmargin 9
set rmargin 0
set output '$2.svg'
red = "#FF0000"; green = "#00FF00"; blue = "#0000FF"; skyblue = "#87CEEB"; violet= "#9400d3"
set xrange [0:60]
set xtics nomirror
set ytics nomirror
set yrange [0:]
set xlabel "Winning Rate (%)"
#set offset -1.3,-0.4,0,0
#set offset -.5,-0.4,0,0
#set logscale y
set style data histogram
set style histogram cluster gap 1
set style fill solid border -1
set boxwidth 0.8
#set xtics rotate by -45 offset -2
#set xtics format ""
#set grid ytics
#set grid xtics
set key left inside top vertical
#set title "Delay Improvements Normalized to TailDrop"

#plot "file" using 0:$3:5:xtic(1) with boxes notitle lc rgb var

##plot "file" using $3:($1=="Sage"?"dark-violet":"blue"):xtic(1) notitle rgb var
##plot "file" using $3:xtic(1) notitle linecolor rgb blue
##    "file_sage" using $3:xtic(1) notitle linecolor rgb "dark-violet"


### Horizontal bar graph

#myColor(col) = column(col)<0 ? 0xff0000 : column(col)==0 ? 0xcccccc : 0x00ff00
BoxWidth = 0.8
BoxYLow(i)  = i - BoxWidth/2.
BoxYHigh(i) = i + BoxWidth/2.

#set style fill transparent solid 0.3
set yrange [:] reverse
unset key
#set offsets 1,1,0.5,0.5
set offsets 0,0,0.5,0.5

plot "file" u (0):0:(0):3:(BoxYLow(\$0)):(BoxYHigh(\$0)):5:ytic(1) w boxxy lc rgb var, \
    '' u 3:0:(sprintf("%.2f%",\$3)) w labels offset  0.5,0 left

END
gnuplot tmp.gpl 1>tmp

rm tmp* file_sage file file1

