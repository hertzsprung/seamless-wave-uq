#!/usr/bin/env python3
import swepc
import numpy as np
import matplotlib.pyplot as plt

g = 9.80665
N = 64
domain = [0.0, 25.0]
dx = (domain[1] - domain[0])/N
dt = 0.02
endTime = 100.0

xCentre = np.linspace(dx/2, domain[1]-dx/2, N)

def stochastic():
    basis = swepc.GaussianHermiteBasis(degree=1)
    solver = swepc.Roe(g)
    riemannEnsemble = swepc.RiemannEnsemble(basis, solver, quadraturePoints=2)
    flux = swepc.Flux(basis, riemannEnsemble)

    flow = swepc.Flow(N, basis)
    flow.upstream_q = [4.42, 0.0]
    flow.downstream_h = [2.0, 0.0]

    flow.z[:,0] = [0.2 - 0.05*(x-10.0)**2 if (x > 8.0 and x < 12.0) else 0.0
            for x in xCentre]
    flow.z[:,1] = [0.3/np.sqrt(2*np.pi)*np.exp(-(1.5*(x-10))**2/2) for x in xCentre]
    flow.h[:,0] = [2.0 - z for z in flow.z[:,0]]

    return swepc.Simulation(g, flux), flow

stochasticSim, stochasticFlow = stochastic()

_, axarr = plt.subplots(3, sharex=True, figsize=(12,10))

def plot():
    stddev = swepc.Stddev(stochasticFlow)

    axarr[0].cla()
    axarr[0].fill_between(xCentre,
            stochasticFlow.z[:,0] - stddev.z,
            stochasticFlow.z[:,0] + stddev.z, 
            color='lightslategray')
    axarr[0].plot(xCentre, stochasticFlow.z[:,0], color='k')
    axarr[0].fill_between(xCentre,
            stochasticFlow.z[:,0] + stochasticFlow.h[:,0] - stddev.h,
            stochasticFlow.z[:,0] + stochasticFlow.h[:,0] + stddev.h, 
            color='lightskyblue')
    axarr[0].plot(xCentre, stochasticFlow.z[:,0] + stochasticFlow.h[:,0], color='mediumblue')
    axarr[0].set_ylim((0,3))
    axarr[0].text(2, 0.75, "$t$ = {0:.3f}".format(t))
    axarr[0].text(2, 0.25, "$cfl$ = {0:.3f}".format(
        dt/dx*stochasticFlow.maxWaveSpeed(g)))

    axarr[1].cla()
    axarr[1].set_ylim((0,6))
    axarr[1].set_ylabel("q")
    axarr[1].fill_between(xCentre,
            stochasticFlow.q[:,0] - stddev.q,
            stochasticFlow.q[:,0] + stddev.q, 
            color='plum')
    axarr[1].plot(xCentre, stochasticFlow.q[:,0], color='purple')

    axarr[2].cla()
    axarr[2].set_ylim((-0.2,1))
    axarr[2].set_ylabel("Fr")
    axarr[2].plot(xCentre, stochasticFlow.q[:,0]/stochasticFlow.h[:,0]/np.sqrt(g*stochasticFlow.h[:,0]), color='C2')

    plt.draw()
    plt.pause(0.001)
    #plt.savefig("/tmp/sim/{0:06.3f}.png".format(t))

c = 0
t = 0.0
plot()
while t < endTime:
    stochasticSim.timestep(stochasticFlow, dx, dt)
    t = t + dt
    c = c + 1
    if c % 4 == 0:
        plot()

plt.show(block=True)
