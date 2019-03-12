set term epslatex color colortext size 3.5,3.7

set xrange [0:1500]
set style data lines
set key noautotitle center right
set style increment userstyles

set style line 1 lc rgb '#BBBBBB'
set style line 2 lc rgb 'black' lw 3
set style line 3 lc rgb '#9acae1'
set style line 4 lc rgb '#2171b5' lw 5
set style line 5 lt 4 dt (2,2.5) lw 5

set multiplot layout 2,1 margin 0.17,0.99,0.07,0.97 spacing 0, 0.1

set label 1 "(a)" at graph 0.02,0.92
set yrange [-1:19]
set ylabel "Elevation (\\si{\\meter})" offset -1, 0
set ytics 5
set mytics 5
set mxtics 2

plot "`echo $uqdata_builddir`/uq/tsengSteadyState-wellBalancedH-3/statistics.dat" using 1:($2-$5):($2+$5) with filledcurves, \
     "`echo $uqdata_builddir`/uq/tsengSteadyState-wellBalancedH-3/statistics.dat" using 1:2 title 'Topography', \
     "`echo $uqdata_builddir`/uq/tsengSteadyState-wellBalancedH-3/derived-statistics.dat" using 1:($2-$3):($2+$3) with filledcurves, \
     "`echo $uqdata_builddir`/uq/tsengSteadyState-wellBalancedH-3/derived-statistics.dat" using 1:2 title 'FV1', \
     "`echo $uqdata_builddir`/uq/tsengSteadyState-wellBalancedH-3/tseng_exact.dat" using 1:($2+$3) title 'Analytic'

set style line 1 lc rgb '#9acae1'
set style line 2 lc rgb '#2171b5' lw 5
set style line 3 lt 4 dt (2,2.5) lw 5

set label 1 "(b)" at graph 0.02,0.92
set xlabel "$x$ (\\si{\\meter})"
set ylabel "Velocity (\\si{\\meter\\per\\second})" offset 1.3,0
set yrange [0:*]
set ytics auto
set mytics 2
set key noautotitle top right

plot "`echo $uqdata_builddir`/uq/tsengSteadyState-wellBalancedH-3/derived-statistics.dat" using 1:($4-$5):($4+$5) with filledcurves, \
     "`echo $uqdata_builddir`/uq/tsengSteadyState-wellBalancedH-3/derived-statistics.dat" using 1:4 ls 2, \
     "`echo $uqdata_builddir`/uq/tsengSteadyState-wellBalancedH-3/tseng_exact.dat" using 1:(0.75/$3)
