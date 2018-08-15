#!/usr/bin/env python3
import swepc
import numpy as np
import matplotlib.pyplot as plt

g = 9.80665
N = 64
domain = [0.0, 25.0]
dx = (domain[1] - domain[0])/N
dt = 0.04
endTime = 40.0

xFace  = np.linspace(domain[0], domain[1], N+1)
xCentre = np.linspace(dx/2, domain[1]-dx/2, N)

def stochastic():
    basis = swepc.GaussianHermiteBasis(degree=3)
    solver = swepc.Roe(g)
    riemannEnsemble = swepc.RiemannEnsemble(basis, solver, quadraturePoints=4)
    flux = swepc.Flux(basis, riemannEnsemble)

    flow = swepc.Flow(N, basis)
    flow.upstream_q = [4.42, 0.0]
    flow.downstream_h = [2.0, 0.0]
    flow.h[:,0] = 2.0
    flow.z[:,0] = [0.2 - 0.05*(x-10.0)**2 if x > 8.0 and x < 12.0 else 0.0
            for x in xFace]

    return swepc.Simulation(flux), flow

stochasticSim, stochasticFlow = stochastic()

def plot():
    plt.figure(1)
    plt.clf()
    stddev = [np.sqrt(var.h) for var in stochasticFlow.variance()]
    plt.plot(xFace, stochasticFlow.z[:,0], color='k')
    plt.fill_between(xCentre, stochasticFlow.h[:,0] - stddev,
            stochasticFlow.h[:,0] + stddev, 
            color='lightskyblue')
    plt.plot(xCentre, stochasticFlow.h[:,0], color='mediumblue')
    plt.ylim((0,8))
    plt.text(2, 0.75, "$t$ = {0:.3f}".format(t))
    plt.text(2, 0.25, "$cfl$ = {0:.3f}".format(
        dt/dx*stochasticFlow.maxWaveSpeed(g)))
    plt.pause(0.01)
    #plt.savefig("/tmp/dam/{0:05.3f}.png".format(t))

t = 0.0
plot()
while t < endTime:
    stochasticSim.timestep(stochasticFlow, dx, dt)
    t = t + dt
    plot()

plt.show(block=True)
