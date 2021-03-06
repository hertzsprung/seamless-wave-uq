set term epslatex color colortext size 3.1,3
set style data lines

set xtics out nomirror
set mxtics 2
set mytics 2

binwidth=0.05
bin(x, width) = width*floor(x/width) + binwidth/2.0

set boxwidth binwidth

stats "`echo $uqdata_builddir`/uq/criticalSteadyState-monteCarlo/sample51.dat" nooutput
N = STATS_records

set xrange [0.9:2.35]
set ylabel "$f_\\eta$" offset 1,0

set multiplot layout 2,1 spacing 0.1,0.12 margin 0.14,0.99,0.06,0.95
set samples 200

set label "(a) $x = \\SI{-37.5}{\\meter}$" at 1.8,13
set yrange [0:15]
set key at 2.35,-8

plot "`echo $uqdata_builddir`/uq/criticalSteadyState-monteCarlo/sample12.dat" using (bin($1+$2,binwidth)):(1.0/N/binwidth) smooth freq with boxes fill solid border -1 fc rgb '#DDDDDD' title 'Monte Carlo', \
     "`echo $uqdata_builddir`/uq/criticalSteadyState-wellBalancedH-1/pdf12.dat" using 1:2 lw 3 lc 1 title 'SG $P = 1$', \
     "`echo $uqdata_builddir`/uq/criticalSteadyState-wellBalancedH-2/pdf12.dat" using 1:2 lw 3 lc 2 title 'SG $P = 2$', \
     "`echo $uqdata_builddir`/uq/criticalSteadyState-wellBalancedH-3/pdf12.dat" using 1:2 lw 3 lc 4 title 'SG $P = 3$'

unset label
set label "(b) $x = \\SI{1.5}{\\meter}$" at 1.9,6
set xlabel "Free-surface elevation (\\si{\\meter})"
set yrange [0:7]
set ylabel "$f_\\eta$" offset 0,0
unset key

plot "`echo $uqdata_builddir`/uq/criticalSteadyState-monteCarlo/sample51.dat" using (bin($1+$2,binwidth)):(1.0/N/binwidth) smooth freq with boxes fill solid border -1 fc rgb '#DDDDDD', \
     "`echo $uqdata_builddir`/uq/criticalSteadyState-wellBalancedH-1/pdf51.dat" using 1:2 lw 3 lc 1, \
     "`echo $uqdata_builddir`/uq/criticalSteadyState-wellBalancedH-2/pdf51.dat" using 1:2 lw 3 lc 2, \
     "`echo $uqdata_builddir`/uq/criticalSteadyState-wellBalancedH-3/pdf51.dat" using 1:2 lw 3 lc 4
