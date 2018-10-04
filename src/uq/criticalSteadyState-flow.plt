set term epslatex color colortext size 3,3.4
set style data lines

set multiplot layout 2,1 spacing 0.1,0.15 margin 0.22,0.85,0.1,0.78

set ytics 0.2 nomirror
set y2tics

set label "(a)" at 38,0.9
set arrow from 1.5,0.8 to 1.5,1.7 lw 6 lc rgbcolor '#999999' nohead
set arrow from -37.5,0.8 to -37.5,1.7 lw 6 lc rgbcolor '#999999' nohead
set xtics 25
set yrange [0.8:1.7]
set y2range [0:0.5]
set key at 50,2.4
set ylabel "Water elevation (\\si{\\meter})"
set y2label "$\\sigma$" offset -2,0
set mytics 2
set my2tics 2

plot "`echo $uqdata_builddir`/uq/criticalSteadyState-wellBalancedEta/statistics.dat" using 1:3 lw 3 lc 1 title 'Stochastic Galerkin mean', \
     "`echo $uqdata_builddir`/uq/criticalSteadyState-monteCarlo/statistics.dat" using 1:3 lw 3 lc 1 dt (2,2) title 'Monte Carlo mean', \
     "`echo $uqdata_builddir`/uq/criticalSteadyState-wellBalancedEta/statistics.dat" using 1:6 lw 3 lc 2 axes x1y2 title 'Stochastic Galerkin $\sigma$', \
     "`echo $uqdata_builddir`/uq/criticalSteadyState-monteCarlo/statistics.dat" using 1:6 axes x1y2 lc 2 dt (2,2) lw 3 title 'Monte Carlo $\sigma$'

unset arrow
set arrow from 1.5,1.5 to 1.5,1.8 lw 6 lc rgbcolor '#999999' nohead
set arrow from -37.5,1.5 to -37.5,1.8 lw 6 lc rgbcolor '#999999' nohead
unset label
set label "(b)" at 38,1.54
set xlabel "$x$ (\\si{\\meter})"
set yrange [1.5:1.8]
set ytics 0.1 nomirror
set y2range [0:0.2]
set y2label offset -3,0
unset key
set ylabel "Discharge (\\si{\\meter\\squared\\per\\second})"
unset mytics
unset my2tics

plot "`echo $uqdata_builddir`/uq/criticalSteadyState-wellBalancedEta/statistics.dat" using 1:4 lc 1 lw 3, \
     "`echo $uqdata_builddir`/uq/criticalSteadyState-wellBalancedEta/statistics.dat" using 1:7 lc 2 lw 3 axes x1y2, \
     "`echo $uqdata_builddir`/uq/criticalSteadyState-monteCarlo/statistics.dat" using 1:4 lc 1 lw 3 dt (2,2), \
     "`echo $uqdata_builddir`/uq/criticalSteadyState-monteCarlo/statistics.dat" using 1:7 axes x1y2 lc 2 lw 3 dt (2,2)
