#!/usr/bin/env python3
import swepc
import numpy as np
import matplotlib.pyplot as plt

g = 9.80665
N = 64
domain = [0.0, 50.0]
dx = (domain[1] - domain[0])/N
dt = 0.04
endTime = 2.5
xs = np.linspace(dx/2, domain[1]-dx/2, N)

basis = swepc.GaussianHermiteBasis(degree=1)
flow = swepc.Flow(N, basis)
flow.h[:,0] = 6.0
flow.h[N//2:,0] = 2.0
flow.h[:,1] = [2/np.sqrt(2*np.pi)*np.exp(-(0.5*(x-25))**2/2) for x in xs]

mc = swepc.MonteCarlo(g)
flow = mc.simulate(flow, dx, dt, endTime, iterations=100)

plt.figure(1)
plt.clf()
plt.fill_between(xs, flow.h[:,0] - flow.h[:,1],
        flow.h[:,0] + flow.h[:,1], 
        color='lightskyblue')
plt.plot(xs, flow.h[:,0], color='mediumblue')
plt.ylim((0,8))
plt.show(block=True)
