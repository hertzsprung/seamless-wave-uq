set style data lines

set xlabel "Water elevation (\\si{\\meter})"

binwidth=0.05
bin(x, width) = width*floor(x/width) + binwidth/2.0

set boxwidth binwidth

set xrange [0.0:2.5]

plot 'build/uq/criticalSteadyState-monteCarlo/sample51.dat' using 1:(0.05) smooth kdensity bandwidth 0.05 notitle, \
     'build/uq/criticalSteadyState-monteCarlo/sample51.dat' using (bin($1,binwidth)):(1.0) smooth freq with boxes notitle, \
     'pdf.dat' using 1:(5*$2) title 'Stochastic Galerkin PDF'
