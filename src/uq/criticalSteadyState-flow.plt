set term epslatex color colortext size 4,2.7

set style data lines

set multiplot layout 2,2 spacing 0.1,0.15 margin 0.16,0.98,0.07,0.88

set xtics 25
set yrange [0:2]
set ylabel "Elevation (\\si{\\meter})"

unset key
set title 'Monte Carlo'
set label "Water elevation" at -47,1.3
set label "Topography" at -47,0.7
set arrow from 1.5,0 to 1.5,2 dt 3 lw 2 lc rgbcolor 'black' nohead

plot "`echo $uqdata_builddir`/uq/criticalSteadyState-monteCarlo/statistics.dat" using 1:($2-$5):($2+$5) with filledcurves lc rgbcolor '#BBBBBB' notitle, \
     "`echo $uqdata_builddir`/uq/criticalSteadyState-monteCarlo/statistics.dat" using 1:2 lc rgbcolor 'black' lw 3 title 'Topography', \
     "`echo $uqdata_builddir`/uq/criticalSteadyState-monteCarlo/statistics.dat" using 1:($3-$6):($3+$6) with filledcurves lw 3 lc rgbcolor '#9acae1' notitle, \
     "`echo $uqdata_builddir`/uq/criticalSteadyState-monteCarlo/statistics.dat" using 1:3 lw 3 lc rgbcolor '#2171b5' title 'Water elevation'

unset label
unset ylabel
unset key

set title 'Stochastic Galerkin'

plot "`echo $uqdata_builddir`/uq/criticalSteadyState-wellBalancedEta/statistics.dat" using 1:($2-$5):($2+$5) with filledcurves lc rgbcolor '#BBBBBB' notitle, \
     "`echo $uqdata_builddir`/uq/criticalSteadyState-wellBalancedEta/statistics.dat" using 1:2 lc rgbcolor 'black' lw 3 title 'Topography', \
     "`echo $uqdata_builddir`/uq/criticalSteadyState-wellBalancedEta/statistics.dat" using 1:($3-$6):($3+$6) with filledcurves lw 3 lc rgbcolor '#9acae1' notitle, \
     "`echo $uqdata_builddir`/uq/criticalSteadyState-wellBalancedEta/statistics.dat" using 1:3 lw 3 lc rgbcolor '#2171b5' title 'Water elevation'

unset arrow
unset title
set yrange [1.5:1.9]
set ytics 0.1
set ylabel "Discharge (\\si{\\meter\\squared\\per\\second})"
set xlabel "$x$ (\\si{\\meter})"

plot "`echo $uqdata_builddir`/uq/criticalSteadyState-monteCarlo/statistics.dat" using 1:($4-$7):($4+$7) with filledcurves lc rgbcolor '#a1d99b' notitle, \
     "`echo $uqdata_builddir`/uq/criticalSteadyState-monteCarlo/statistics.dat" using 1:4 lc rgbcolor '#238b45' lw 3

unset ylabel

plot "`echo $uqdata_builddir`/uq/criticalSteadyState-wellBalancedEta/statistics.dat" using 1:($4-$7):($4+$7) with filledcurves lc rgbcolor '#a1d99b' notitle, \
     "`echo $uqdata_builddir`/uq/criticalSteadyState-wellBalancedEta/statistics.dat" using 1:4 lc rgbcolor '#238b45' lw 3
