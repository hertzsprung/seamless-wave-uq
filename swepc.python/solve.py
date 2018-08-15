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

def deterministic():
    basis = swepc.GaussianHermiteBasis(degree=0)
    solver = swepc.Roe(g)
    riemannEnsemble = swepc.RiemannEnsemble(basis, solver, quadraturePoints=1)
    flux = swepc.Flux(basis, riemannEnsemble)

    flow = swepc.Flow(N, basis)
    flow.h[:,0] = 6.0
    flow.h[N//2:,0] = 2.0

    return swepc.Simulation(flux), flow

def stochastic():
    basis = swepc.GaussianHermiteBasis(degree=3)
    solver = swepc.Roe(g)
    riemannEnsemble = swepc.RiemannEnsemble(basis, solver, quadraturePoints=4)
    flux = swepc.Flux(basis, riemannEnsemble)

    flow = swepc.Flow(N, basis)
    flow.h[:,0] = 6.0
    flow.h[N//2:,0] = 2.0
    flow.h[:,1] = [2/np.sqrt(2*np.pi)*np.exp(-(0.5*(x-25))**2/2) for x in xs]

    return swepc.Simulation(flux), flow

deterministicSim, deterministicFlow = deterministic()
stochasticSim, stochasticFlow = stochastic()

def plot():
    plt.figure(1)
    plt.clf()
#    plt.fill_between(xs, stochasticFlow.h[:,0] - stochasticFlow.h[:,1],
#            stochasticFlow.h[:,0] + stochasticFlow.h[:,1], 
#            color='lightskyblue')
    stddev = [np.sqrt(var.h) for var in stochasticFlow.variance()]
    plt.fill_between(xs, stochasticFlow.h[:,0] - stddev,
            stochasticFlow.h[:,0] + stddev, 
            color='lightskyblue')
    plt.plot(xs, stochasticFlow.h[:,0], color='mediumblue')
    #plt.plot(xs, deterministicFlow.h[:,0], color='magenta', linewidth=0.5)
    plt.ylim((0,8))
    plt.text(2, 0.75, "$t$ = {0:.3f}".format(t))
    plt.text(2, 0.25, "$cfl$ = {0:.3f}".format(
        dt/dx*stochasticFlow.maxWaveSpeed(g)))
    plt.pause(0.01)
    #plt.savefig("/tmp/dam/{0:05.3f}.png".format(t))

t = 0.0
plot()
while t < endTime:
    #deterministicSim.timestep(deterministicFlow, dx, dt)
    stochasticSim.timestep(stochasticFlow, dx, dt)
    t = t + dt
    plot()

plt.show(block=True)
