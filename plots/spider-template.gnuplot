unset border
set grid nopolar
set grid noxtics nomxtics noytics nomytics noztics nomztics nortics nomrtics \
 nox2tics nomx2tics noy2tics nomy2tics nocbtics nomcbtics
set grid back   linecolor rgb "grey"  linewidth 0.500 dashtype solid,  linecolor rgb "grey"  linewidth 0.500 dashtype solid
set key fixed bottom center horizontal noreverse enhanced noautotitle outside box height 1 width 1
set spiderplot
set style spiderplot  linewidth 1.000 dashtype solid pointtype 6 pointsize 2.000
set style spiderplot fillstyle  transparent solid 0.10 border
set size ratio 1 1,1
set style data spiderplot
unset xtics
unset ytics
unset ztics
unset cbtics
unset rtics
set paxis 1 tics axis in scale 1,.5 nomirror norotate  autojustify
set paxis 1 tics  norangelimit autofreq  font ",9"
set paxis 2 tics axis in scale 1,.5 nomirror norotate  autojustify
set paxis 2 tics  norangelimit autofreq  font ",9"
set paxis 3 tics axis in scale 1,.5 nomirror norotate  autojustify
set paxis 3 tics  norangelimit autofreq  font ",9"
set paxis 4 tics axis in scale 1,.5 nomirror norotate  autojustify
set paxis 4 tics  norangelimit autofreq  font ",9"
set paxis 5 tics axis in scale 1,.5 nomirror norotate  autojustify
set paxis 5 tics  norangelimit autofreq  font ",9"
unset paxis 6 tics 
unset paxis 7 tics
unset paxis 8 tics
unset paxis 9 tics
unset paxis 10 tics
set xrange [ * : * ] noreverse writeback
set x2range [ * : * ] noreverse writeback
set yrange [ * : * ] noreverse writeback
set y2range [ * : * ] noreverse writeback
set zrange [ * : * ] noreverse writeback
set cbrange [ * : * ] noreverse writeback
set rrange [ * : * ] noreverse writeback
set paxis 1 range [ 0:485 ]  noextend
set paxis 1 label "Population" 
set paxis 1 label  font "" textcolor lt -1 norotate
set paxis 2 range [ 0.0:0.5 ]  noextend
set paxis 2 label "Elite Ratio" 
set paxis 2 label  font "" textcolor lt -1 norotate
set paxis 3 range [ 0.0:0.5 ]  noextend
set paxis 3 label "Crossover" 
set paxis 3 label  font "" textcolor lt -1 norotate
set paxis 4 range [ 0.0:0.2 ]  noextend
set paxis 4 label "Mutation Rate" 
set paxis 4 label  font "" textcolor lt -1 norotate
set paxis 5 range [ 0.0:.22 ]  noextend
set paxis 5 label "Mutation Change" 
set paxis 5 label  font "" textcolor lt -1 norotate
set paxis 6 range [ 0:5 ]  noextend
set paxis 7 range [ 0:5 ]  noextend
set paxis 8 range [ 0:5 ]  noextend
set paxis 9 range [ 0:5 ]  noextend
set paxis 10 range [ 0:5 ]  noextend
NO_ANIMATION = 1



set style line 1 lc rgb "#55774444" lw 2 pt 12 ps 2
set style line 2 lc rgb "#55994444" lw 2 pt 4 ps 2
set style line 3 lc rgb "#55bb4444" lw 2 pt 5 ps 2
set style line 4 lc rgb "#55dd4444" lw 2 pt 10 ps 2
set style line 5 lc rgb "#55ff4444" lw 2 pt 8 ps 2
set style line 6 lc rgb "#55000020" lw 2 pt 12 ps 2
set style line 7 lc rgb "#55000040" lw 2 pt 4 ps 2
set style line 8 lc rgb "#55000080" lw 2 pt 5 ps 2
set style line 9 lc rgb "#550000c0" lw 2 pt 10 ps 2
set style line 10 lc rgb "#550000ff" lw 2 pt 8 ps 2

set style parallelaxis lw 0.5