set style data lines

plot 'build/uq/criticalSteadyState-wellBalancedEta/statistics.dat' using 1:3 title 'SG mean', \
     'build/uq/criticalSteadyState-wellBalancedEta/statistics.dat' using 1:6 title 'SG stddev', \
     'build/uq/criticalSteadyState-wellBalancedEta/statistics.dat' using 1:9 title 'SG skew', \
     'build/uq/criticalSteadyState-wellBalancedEta/statistics.dat' using 1:12 title 'SG kurtosis', \
     'build/uq/criticalSteadyState-monteCarlo/statistics.dat' using 1:3 lc 1 dt 2 title 'MC mean', \
     'build/uq/criticalSteadyState-monteCarlo/statistics.dat' using 1:6 lc 2 dt 2 title 'MC stddev', \
     'build/uq/criticalSteadyState-monteCarlo/statistics.dat' using 1:9 lc 3 dt 2 title 'MC skew', \
     'build/uq/criticalSteadyState-monteCarlo/statistics.dat' using 1:12 lc 4 dt 2 title 'MC kurtosis'
