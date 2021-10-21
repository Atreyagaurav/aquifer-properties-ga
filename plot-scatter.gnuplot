set datafile separator ","

set grid linetype 4 dashtype 2 linecolor '#aaaaaa'

# set title "Stream Flow in two stations (08171000 & 08172000)"

# variables
csvfile="./data.csv"

set style line 1 lt 1 lc '#0000ff' lw 2
set style line 2 lt 1 lc '#ff0000' lw 2

# set terminal png size 700,300

# set output "./graphics/plot-discharge.png" 
set ylabel "drawdown"
set xlabel "time"
set logscale x
set logscale y
set key on title ""
set yrange [0.01:1]
set xrange [0.1:500]

Q = 8.155
r = 582
S = 4.2E-05
T = 5.445
PI = 3.141592653589793
E = 0.57721

Cut = r*r*S/(4*T)
Csrt = Q/(4*PI*T)

plot csvfile u "time":"drawdown" w points ls 1 t "obs data",\
     Csrt * (-log(Cut/x) - E + (Cut/x) - (Cut/x)*(Cut/x)/4) w lines ls 2

