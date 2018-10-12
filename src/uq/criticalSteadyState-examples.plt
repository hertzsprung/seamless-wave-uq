set term epslatex color colortext size 6,3
set style data lines

set yrange [0:2.3]
set xlabel "$x$ (\\si{\\meter})"
set ylabel "Elevation (\\si{\\meter})"

plot "`echo $uqdata_builddir`/uq/criticalSteadyState-deterministic-sigma/statistics.dat" using 1:($2+$3) lw 4 title '$\overline{a} - \sigma_a$', \
     "`echo $uqdata_builddir`/uq/criticalSteadyState-deterministic-mean/statistics.dat" using 1:($2+$3) lw 4 title '$\overline{a}$', \
     "`echo $uqdata_builddir`/uq/criticalSteadyState-deterministic+sigma/statistics.dat" using 1:($2+$3) lw 4 title '$\overline{a} + \sigma_a$', \
     "`echo $uqdata_builddir`/uq/criticalSteadyState-deterministic+2sigma/statistics.dat" using 1:($2+$3) lw 4 title '$\overline{a} + 2\sigma_a$', \
     "`echo $uqdata_builddir`/uq/criticalSteadyState-deterministic-sigma/statistics.dat" using 1:2 lc 1 notitle, \
     "`echo $uqdata_builddir`/uq/criticalSteadyState-deterministic-mean/statistics.dat" using 1:2 lc 2 notitle, \
     "`echo $uqdata_builddir`/uq/criticalSteadyState-deterministic+sigma/statistics.dat" using 1:2 lc 3 notitle, \
     "`echo $uqdata_builddir`/uq/criticalSteadyState-deterministic+2sigma/statistics.dat" using 1:2 lc 4 notitle
