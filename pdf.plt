set xlabel "Water elevation (\\si{\\meter})"

plot 'build/uq/criticalSteadyState-monteCarlo/sample.dat' using 2:(2) smooth kdensity bandwidth 0.05 notitle
