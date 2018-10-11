set term epslatex color colortext size 3.1,3
set style data lines

binwidth=0.05
bin(x, width) = width*floor(x/width) + binwidth/2.0

set boxwidth binwidth

stats "`echo $uqdata_builddir`/uq/criticalSteadyState-monteCarlo/sample51.dat" nooutput
N = STATS_records

set xrange [0.1:2.1]
set ylabel "$f(\\eta)$" offset 1,0

set multiplot layout 2,1 spacing 0.1,0.12 margin 0.14,0.99,0.05,0.95
set samples 200

set label "(a) $x = \\SI{-37.5}{\\meter}$" at 1.6,13
set yrange [0:15]
set key at 1.5,14 samplen 1.5

plot "`echo $uqdata_builddir`/uq/criticalSteadyState-monteCarlo/sample12.dat" using (bin($2,binwidth)):(1.0/N/binwidth) smooth freq with boxes fill solid border -1 fc rgb '#DDDDDD' title 'Monte Carlo', \
     "`echo $uqdata_builddir`/uq/criticalSteadyState-wellBalancedH/pdf12.dat" using 1:2 lw 3 lc rgb 'black' title 'Stochastic Galerkin'

unset label
set label "(b) $x = \\SI{1.5}{\\meter}$" at 1.68,6
set xlabel "Water height (\\si{\\meter})"
set yrange [0:7]
set ylabel "$f(\\eta)$" offset 0,0
unset key

plot "`echo $uqdata_builddir`/uq/criticalSteadyState-monteCarlo/sample51.dat" using (bin($2,binwidth)):(1.0/N/binwidth) smooth freq with boxes fill solid border -1 fc rgb '#DDDDDD', \
     "`echo $uqdata_builddir`/uq/criticalSteadyState-wellBalancedH/pdf51.dat" using 1:2 lw 3 lc rgb 'black'
