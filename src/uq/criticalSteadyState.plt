set term epslatex color colortext size 4,4.5

set style data lines

set multiplot layout 3,2 spacing 0.08,0.1 margin 0.12,0.98,0.07,0.9

set xtics 25
set yrange [0:2]
set ylabel "Elevation (\\si{\\meter})"

unset key
set title 'Centred difference $\eta$-form'
set label "Water elevation" at -47,1.3
set label "Topography" at -47,0.7

plot "`echo $uqdata_builddir`/uq/criticalSteadyState-centredDifferenceEta.dat" using 1:($2-$5):($2+$5) with filledcurves lc rgbcolor '#BBBBBB' notitle, \
     "`echo $uqdata_builddir`/uq/criticalSteadyState-centredDifferenceEta.dat" using 1:2 lc rgbcolor 'black' lw 3 title 'Topography', \
     "`echo $uqdata_builddir`/uq/criticalSteadyState-centredDifferenceEta.dat" using 1:($3-$6):($3+$6) with filledcurves lw 3 lc rgbcolor '#9acae1' notitle, \
     "`echo $uqdata_builddir`/uq/criticalSteadyState-centredDifferenceEta.dat" using 1:3 lw 3 lc rgbcolor '#2171b5' title 'Water elevation'

unset ylabel
unset key

set title 'Well-balanced $\eta$-form'

plot "`echo $uqdata_builddir`/uq/criticalSteadyState-wellBalancedEta.dat" using 1:($2-$5):($2+$5) with filledcurves lc rgbcolor '#BBBBBB' notitle, \
     "`echo $uqdata_builddir`/uq/criticalSteadyState-wellBalancedEta.dat" using 1:2 lc rgbcolor 'black' lw 3 title 'Topography', \
     "`echo $uqdata_builddir`/uq/criticalSteadyState-wellBalancedEta.dat" using 1:($3-$6):($3+$6) with filledcurves lw 3 lc rgbcolor '#9acae1' notitle, \
     "`echo $uqdata_builddir`/uq/criticalSteadyState-wellBalancedEta.dat" using 1:3 lw 3 lc rgbcolor '#2171b5' title 'Water elevation'

unset title
set yrange [1.2:2]
set ylabel "Discharge (\\si{\\meter\\squared\\per\\second})"
set xlabel "$x$ (\\si{\\meter})"

plot "`echo $uqdata_builddir`/uq/criticalSteadyState-centredDifferenceEta.dat" using 1:($4-$7):($4+$7) with filledcurves lc rgbcolor '#a1d99b' notitle, \
     "`echo $uqdata_builddir`/uq/criticalSteadyState-centredDifferenceEta.dat" using 1:4 lc rgbcolor '#238b45' lw 3

plot "`echo $uqdata_builddir`/uq/criticalSteadyState-wellBalancedEta.dat" using 1:($4-$7):($4+$7) with filledcurves lc rgbcolor '#a1d99b' notitle, \
     "`echo $uqdata_builddir`/uq/criticalSteadyState-wellBalancedEta.dat" using 1:4 lc rgbcolor '#238b45' lw 3
