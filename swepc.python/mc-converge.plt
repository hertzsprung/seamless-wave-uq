set style data lines

set logscale x

set multiplot layout 1,2
set ytics nomirror
set y2tics

plot 'mc-converge.dat' using 1:2, 'mc-converge.dat' using 1:3 axes x1y2

set logscale y
unset y2tics
set ytics mirror

plot 'mc-converge.dat' using 1:4, 5e-2/sqrt(x)
