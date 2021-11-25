set  logscale x
set  logscale y

set key on left opaque box

plot "./data/gen-0000.txt" u 1:2 w points, \
     "./data/gen-0010.txt" u 1:2 w point, \
     "./data/gen-0100.txt" u 1:2 w points lc "red",\
     "./data/gen-0999.txt" u 1:2 w points
