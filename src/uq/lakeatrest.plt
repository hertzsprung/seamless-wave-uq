set term epslatex color colortext size 4.5,3.7

set style data lines

set multiplot layout 2,2 spacing 0.2,0.1 margin 0.13,0.98,0.07,0.9

set xtics 25
set yrange [0:2]
set ylabel "Elevation (\\si{\\meter})" offset 0.5,0

unset key
set title 'Centred difference'
set label "(a)" at -46,1.8
set label "Water elevation" at -47,1.3
set label "Topography" at -47,0.7

plot "`echo $uqdata_builddir`/uq/lakeAtRest-centredDifferenceH/statistics.dat" using 1:($2-$5):($2+$5) with filledcurves lc rgbcolor '#BBBBBB' notitle, \
     "`echo $uqdata_builddir`/uq/lakeAtRest-centredDifferenceH/statistics.dat" using 1:2 lc rgbcolor 'black' lw 3 title 'Topography', \
     "`echo $uqdata_builddir`/uq/lakeAtRest-centredDifferenceH/derived-statistics.dat" using 1:($2-$3):($2+$3) with filledcurves lw 3 lc rgbcolor '#9acae1' notitle, \
     "`echo $uqdata_builddir`/uq/lakeAtRest-centredDifferenceH/derived-statistics.dat" using 1:2 lw 3 lc rgbcolor '#2171b5' title 'Water elevation'

unset label
set label "(b)" at -46,1.8
unset ylabel
unset key
set title 'Surface gradient method'

plot "`echo $uqdata_builddir`/uq/lakeAtRest-wellBalancedH/statistics.dat" using 1:($2-$5):($2+$5) with filledcurves lc rgbcolor '#BBBBBB' notitle, \
     "`echo $uqdata_builddir`/uq/lakeAtRest-wellBalancedH/statistics.dat" using 1:2 lc rgbcolor 'black' lw 3 title 'Topography', \
     "`echo $uqdata_builddir`/uq/lakeAtRest-wellBalancedH/derived-statistics.dat" using 1:($2-$3):($2+$3) with filledcurves lw 3 lc rgbcolor '#9acae1' notitle, \
     "`echo $uqdata_builddir`/uq/lakeAtRest-wellBalancedH/derived-statistics.dat" using 1:2 lw 3 lc rgbcolor '#2171b5' title 'Water elevation'

unset title
set yrange [-1:1]
set ylabel "Discharge (\\si{\\meter\\squared\\per\\second})" offset 1.5,0
set xlabel "$x$ (\\si{\\meter})"
unset label
set label "(c)" at -46,0.8

plot "`echo $uqdata_builddir`/uq/lakeAtRest-centredDifferenceH/statistics.dat" using 1:($4-$7):($4+$7) with filledcurves lc rgbcolor '#a1d99b' notitle, \
     "`echo $uqdata_builddir`/uq/lakeAtRest-centredDifferenceH/statistics.dat" using 1:4 lc rgbcolor '#238b45' lw 3

unset ylabel
unset label
set label "(d)" at -46,1.6e-14
set yrange [-2e-14:2e-14]
set ytics 1e-14

plot "`echo $uqdata_builddir`/uq/lakeAtRest-wellBalancedH/statistics.dat" using 1:($4-$7):($4+$7) with filledcurves lc rgbcolor '#a1d99b' notitle, \
     "`echo $uqdata_builddir`/uq/lakeAtRest-wellBalancedH/statistics.dat" using 1:4 lc rgbcolor '#238b45' lw 3
