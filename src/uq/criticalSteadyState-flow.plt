set term epslatex color colortext size 6,3
set style data lines

set lmargin screen 0.1
set rmargin screen 0.98

set arrow from 1.5, graph 0 to 1.5, graph 1 lw 5 lc rgbcolor '#666666' dt (1, 2) nohead
set arrow from -37.5, graph 0 to -37.5, graph 1 lw 5 lc rgbcolor '#666666' dt (1, 2) nohead
set xtics 25
set yrange [0:2]
set key outside top center
set key at 18,0.85
set xlabel "$x$ (\\si{\\meter})"
set ylabel "Elevation (\\si{\\meter})" offset 1,0
set mytics 2

plot "`echo $uqdata_builddir`/uq/criticalSteadyState-wellBalancedH-3/statistics.dat" using 1:($2-$5):($2+$5) with filledcurves lc rgbcolor '#BBBBBB' notitle, \
     "`echo $uqdata_builddir`/uq/criticalSteadyState-wellBalancedH-3/statistics.dat" using 1:2 lc rgbcolor 'black' lw 4 title 'Mean topography $\overline{z}$', \
     NaN with filledcurves lc rgbcolor '#BBBBBB' title 'Std. deviation in topography $\sigma_z$', \
     "`echo $uqdata_builddir`/uq/criticalSteadyState-wellBalancedH-3/derived-statistics.dat" using 1:($2-$3):($2+$3) with filledcurves lw 3 lc rgbcolor '#b0d6e8' notitle, \
     NaN lw 6 lc rgbcolor '#0072d3' title 'Stochastic Galerkin $\overline{\eta}$', \
     NaN with filledcurves lw 3 lc rgbcolor '#b0d6e8' title 'Stochastic Galerkin $\sigma_\eta$', \
     "`echo $uqdata_builddir`/uq/criticalSteadyState-monteCarlo/derived-statistics.dat" using 1:2 with points lc 7 lw 2 pt 7 ps 1 title 'Monte Carlo $\overline{\eta}$', \
     "`echo $uqdata_builddir`/uq/criticalSteadyState-wellBalancedH-3/derived-statistics.dat" using 1:2 lw 6 lc rgbcolor '#0072d3' notitle, \
     "`echo $uqdata_builddir`/uq/criticalSteadyState-monteCarlo/derived-statistics.dat" using 1:($2-$3) lw 4 lc 7 dt (3, 2) title 'Monte Carlo $\sigma_\eta$', \
     "`echo $uqdata_builddir`/uq/criticalSteadyState-monteCarlo/derived-statistics.dat" using 1:($2+$3) lw 4 lc 7 dt (3, 2) notitle
