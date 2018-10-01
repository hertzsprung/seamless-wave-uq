set style data points

set logscale

set yrange [*:1e-2]

f(x) = a/sqrt(x)
a=1e-3
#fit f(x) 'mc-converge.dat' using 1:2 via a

plot 'mc-converge.dat' using 1:2, 'mc-converge.dat' using 1:3, 1e-2/x
