set term epslatex color colortext size 3,3.5
set style data lines

set lmargin screen 0.18
set rmargin 0.1

set arrow from 1.5, graph 0 to 1.5, graph 1 lw 4 lc rgbcolor '#666666' dt (1, 2) nohead
set arrow from -37.5, graph 0 to -37.5, graph 1 lw 4 lc rgbcolor '#666666' dt (1, 2) nohead
set xtics 25
set yrange [0:2]
set key outside top center
#set key at 50,2.4
set xlabel "$x$ (\\si{\\meter})"
set ylabel "Water elevation (\\si{\\meter})" offset 1,0
set mytics 2

plot "`echo $uqdata_builddir`/uq/criticalSteadyState-wellBalancedH/statistics.dat" using 1:($2-$5):($2+$5) with filledcurves lc rgbcolor '#BBBBBB' notitle, \
     "`echo $uqdata_builddir`/uq/criticalSteadyState-wellBalancedH/statistics.dat" using 1:2 lc rgbcolor 'black' lw 3 title 'Topography', \
     "`echo $uqdata_builddir`/uq/criticalSteadyState-wellBalancedH/derived-statistics.dat" using 1:($2-$3):($2+$3) with filledcurves lw 3 lc rgbcolor '#b0d6e8' notitle, \
     "`echo $uqdata_builddir`/uq/criticalSteadyState-wellBalancedH/derived-statistics.dat" using 1:2 lw 3 lc rgbcolor '#0072d3' title 'Stochastic Galerkin mean $\eta$', \
     NaN with filledcurves lw 3 lc rgbcolor '#b0d6e8' title 'Stochastic Galerkin $\sigma_\eta$', \
     "`echo $uqdata_builddir`/uq/criticalSteadyState-monteCarlo/derived-statistics.dat" using 1:2 lw 4 lc rgbcolor '#08519c' dt (2,2) title 'Monte Carlo mean $\eta$', \
     "`echo $uqdata_builddir`/uq/criticalSteadyState-monteCarlo/derived-statistics.dat" using 1:($2-$3) lw 2.5 lc rgbcolor '#08519c' title 'Monte Carlo $\sigma_\eta$', \
     "`echo $uqdata_builddir`/uq/criticalSteadyState-monteCarlo/derived-statistics.dat" using 1:($2+$3) lw 2.5 lc rgbcolor '#08519c' notitle
