set term epslatex color colortext size 6,3
set style data lines

set yrange [0:2.3]
set xlabel "$x$ (\\si{\\meter})"
set ylabel "Elevation (\\si{\\meter})"

set arrow from 1.5, graph 0 to 1.5, graph 1 lw 5 lc rgbcolor '#666666' dt (1, 2) nohead
set arrow from -37.5, graph 0 to -37.5, graph 1 lw 5 lc rgbcolor '#666666' dt (1, 2) nohead

plot "`echo $uqdata_builddir`/uq/criticalSteadyState-deterministic-sigma/statistics.dat" using 1:($2+$3) lw 4 title '$\overline{r} - \sigma_r = \SI{0.3}{\meter}$', \
     "`echo $uqdata_builddir`/uq/criticalSteadyState-deterministic-mean/statistics.dat" using 1:($2+$3) lw 4 title '$\overline{r}$ = \SI{0.6}{\meter}', \
     "`echo $uqdata_builddir`/uq/criticalSteadyState-deterministic+sigma/statistics.dat" using 1:($2+$3) lw 4 title '$\overline{r} + \sigma_r = \SI{0.9}{\meter}$', \
     "`echo $uqdata_builddir`/uq/criticalSteadyState-deterministic+2sigma/statistics.dat" using 1:($2+$3) lw 4 title '$\overline{r} + 2\sigma_r = \SI{1.2}{\meter}$', \
     "`echo $uqdata_builddir`/uq/criticalSteadyState-deterministic-sigma/statistics.dat" using 1:2 lc 1 lw 4 dt (5,1.5) notitle, \
     "`echo $uqdata_builddir`/uq/criticalSteadyState-deterministic-mean/statistics.dat" using 1:2 lc 2 lw 4 dt (5,1.5) notitle, \
     "`echo $uqdata_builddir`/uq/criticalSteadyState-deterministic+sigma/statistics.dat" using 1:2 lc 3 lw 4 dt (5,1.5) notitle, \
     "`echo $uqdata_builddir`/uq/criticalSteadyState-deterministic+2sigma/statistics.dat" using 1:2 lc 4 lw 4 dt (5,1.5) notitle
