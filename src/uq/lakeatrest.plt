set term epslatex color colortext size 6.5,3.7

set style data lines

set multiplot layout 2,3 spacing 0.08,0.1 margin 0.12,0.98,0.07,0.9

set xtics 25
set yrange [0:2]
set ylabel "Elevation (\\si{\\meter})"

unset key
set title 'Centred difference $\eta$-form'
set label "(a)" at -47,1.8
set label "Water elevation" at -47,1.3
set label "Topography" at -47,0.7

plot "`echo $uqdata_builddir`/uq/lakeAtRest-centredDifferenceEta.dat" using 1:($2-$5):($2+$5) with filledcurves lc rgbcolor '#BBBBBB' notitle, \
     "`echo $uqdata_builddir`/uq/lakeAtRest-centredDifferenceEta.dat" using 1:2 lc rgbcolor 'black' lw 3 title 'Topography', \
     "`echo $uqdata_builddir`/uq/lakeAtRest-centredDifferenceEta.dat" using 1:($3-$6):($3+$6) with filledcurves lw 3 lc rgbcolor '#9acae1' notitle, \
     "`echo $uqdata_builddir`/uq/lakeAtRest-centredDifferenceEta.dat" using 1:3 lw 3 lc rgbcolor '#2171b5' title 'Water elevation'

unset label
set label "(b)" at -47,1.8
unset ylabel
unset key
set title 'Well-balanced $h$-form'

plot "`echo $uqdata_builddir`/uq/lakeAtRest-wellBalancedH.dat" using 1:($2-$5):($2+$5) with filledcurves lc rgbcolor '#BBBBBB' notitle, \
     "`echo $uqdata_builddir`/uq/lakeAtRest-wellBalancedH.dat" using 1:2 lc rgbcolor 'black' lw 3 title 'Topography', \
     "`echo $uqdata_builddir`/uq/lakeAtRest-wellBalancedH.dat" using 1:($2+$3-$6):($2+$3+$6) with filledcurves lw 3 lc rgbcolor '#9acae1' notitle, \
     "`echo $uqdata_builddir`/uq/lakeAtRest-wellBalancedH.dat" using 1:($2+$3) lw 3 lc rgbcolor '#2171b5' title 'Water elevation'

set title 'Well-balanced $\eta$-form'
unset label
set label "(c)" at -47,1.8

plot "`echo $uqdata_builddir`/uq/lakeAtRest-wellBalancedEta.dat" using 1:($2-$5):($2+$5) with filledcurves lc rgbcolor '#BBBBBB' notitle, \
     "`echo $uqdata_builddir`/uq/lakeAtRest-wellBalancedEta.dat" using 1:2 lc rgbcolor 'black' lw 3 title 'Topography', \
     "`echo $uqdata_builddir`/uq/lakeAtRest-wellBalancedEta.dat" using 1:($3-$6):($3+$6) with filledcurves lw 3 lc rgbcolor '#9acae1' notitle, \
     "`echo $uqdata_builddir`/uq/lakeAtRest-wellBalancedEta.dat" using 1:3 lw 3 lc rgbcolor '#2171b5' title 'Water elevation'

unset title
set yrange [-1:1]
set ylabel "Discharge (\\si{\\meter\\squared\\per\\second})"
set xlabel "$x$ (\\si{\\meter})"
unset label
set label "(d)" at -47,0.8

plot "`echo $uqdata_builddir`/uq/lakeAtRest-centredDifferenceEta.dat" using 1:($4-$7):($4+$7) with filledcurves lc rgbcolor '#a1d99b' notitle, \
     "`echo $uqdata_builddir`/uq/lakeAtRest-centredDifferenceEta.dat" using 1:4 lc rgbcolor '#238b45' lw 3

unset ylabel
unset label
set label "(e)" at -47,0.8

plot "`echo $uqdata_builddir`/uq/lakeAtRest-wellBalancedH.dat" using 1:($4-$7):($4+$7) with filledcurves lc rgbcolor '#a1d99b' notitle, \
     "`echo $uqdata_builddir`/uq/lakeAtRest-wellBalancedH.dat" using 1:4 lc rgbcolor '#238b45' lw 3

unset label
set label "(f)" at -47,0.8

plot "`echo $uqdata_builddir`/uq/lakeAtRest-wellBalancedEta.dat" using 1:($4-$7):($4+$7) with filledcurves lc rgbcolor '#a1d99b' notitle, \
     "`echo $uqdata_builddir`/uq/lakeAtRest-wellBalancedEta.dat" using 1:4 lc rgbcolor '#238b45' lw 3
