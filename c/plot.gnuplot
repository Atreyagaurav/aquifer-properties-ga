set  logscale x
set  logscale y

plot "./data/gen-0000.txt" u 1:2 w points, \
     "./data/gen-0010.txt" u 1:2 w point, \
     "./data/gen-0100.txt" u 1:2 w points,\
     "./data/gen-1000.txt" u 1:2 w points
