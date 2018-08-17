#!/usr/bin/env python3
import swepc
import numpy as np
import matplotlib.pyplot as plt

def intrusivePC(initialConditions, boundaryConditions, degree):
    basis = swepc.GaussianHermiteBasis(degree)
    solver = swepc.Roe(g)
    riemannEnsemble = swepc.RiemannEnsemble(
            basis, solver, quadraturePoints=degree+1)
    flux = swepc.Flux(basis, riemannEnsemble)
    flow = swepc.Flow(basis, initialConditions, boundaryConditions)

    return swepc.Simulation(g, flux), flow

def plotPC():
    stddev = swepc.Stddev(pcFlow)

    axarr[0].cla()
    axarr[0].set_ylim((0,3))
    axarr[0].fill_between(xCentre,
            pcFlow.z[:,0] - stddev.z,
            pcFlow.z[:,0] + stddev.z, 
            color='lightslategray')
    axarr[0].plot(xCentre, pcFlow.z[:,0], color='k')
    axarr[0].fill_between(xCentre,
            pcFlow.z[:,0] + pcFlow.h[:,0] - stddev.h,
            pcFlow.z[:,0] + pcFlow.h[:,0] + stddev.h, 
            color='lightskyblue')
    axarr[0].plot(xCentre, pcFlow.z[:,0] + pcFlow.h[:,0], color='mediumblue')
    axarr[0].text(2, 0.75, "$t$ = {0:.3f}".format(t))
    axarr[0].text(2, 0.25, "$cfl$ = {0:.3f}".format(
        dt/dx*pcFlow.maxWaveSpeed(g)))

    axarr[1].cla()
    axarr[1].set_ylim((0,7))
    axarr[1].set_ylabel("q")
    axarr[1].fill_between(xCentre,
            pcFlow.q[:,0] - stddev.q,
            pcFlow.q[:,0] + stddev.q, 
            color='plum')
    axarr[1].plot(xCentre, pcFlow.q[:,0], color='purple')

    axarr[2].cla()
    axarr[2].set_ylim((-0.2,1))
    axarr[2].set_ylabel("Fr")
    axarr[2].plot(xCentre, pcFlow.q[:,0]/pcFlow.h[:,0]/np.sqrt(g*pcFlow.h[:,0]), color='C2')

    plt.draw()
    plt.pause(0.001)
    #plt.savefig("/tmp/sim/{0:06.3f}.png".format(t))

def plotMC():
    stats = swepc.MonteCarloFlowStatistics(mcFlow)

    axarr[0].cla()
    axarr[0].set_ylim((0,3))
    axarr[0].fill_between(xCentre,
            stats.z[:,0] - stats.z[:,1],
            stats.z[:,0] + stats.z[:,1], 
            color='lightslategray')
    axarr[0].plot(xCentre, stats.z[:,0], color='k')

    for flow in mcFlow:
        axarr[0].plot(xCentre, flow.z[:,0] + flow.h[:,0], color='lightgray', lw=0.5)
    axarr[0].fill_between(xCentre,
            stats.z[:,0] + stats.h[:,0] - stats.h[:,1],
            stats.z[:,0] + stats.h[:,0] + stats.h[:,1], 
            color='lightskyblue')
    axarr[0].plot(xCentre, stats.z[:,0] + stats.h[:,0], color='mediumblue')
    axarr[0].text(2, 0.75, "$t$ = {0:.3f}".format(t))

    axarr[1].cla()
    axarr[1].set_ylim((0,7))
    axarr[1].set_ylabel("q")
    axarr[1].fill_between(xCentre,
            stats.q[:,0] - stats.q[:,1],
            stats.q[:,0] + stats.q[:,1], 
            color='plum')
    axarr[1].plot(xCentre, stats.q[:,0], color='purple')

    plt.draw()
    plt.pause(0.001)

g = 9.80665
N = 64
domain = [0.0, 25.0]
dx = (domain[1] - domain[0])/N
dt = 0.03
endTime = 50.0

xCentre = np.linspace(dx/2, domain[1]-dx/2, N)

ic = swepc.InitialConditions(N, degree=1)
ic.z[:,0] = [0.2 - 0.05*(x-10.0)**2 if (x > 8.0 and x < 12.0) else 0.0
        for x in xCentre]
ic.z[:,1] = [0.3/np.sqrt(2*np.pi)*np.exp(-(1.5*(x-10))**2/2) for x in xCentre]
ic.h[:,0] = [2.0 - z for z in ic.z[:,0]]

bc = swepc.BoundaryConditions()
bc.upstream_q = [4.42, 0.0]
bc.downstream_h = [2.0, 0.0]

pcSim, pcFlow = intrusivePC(ic, bc, degree=3)
mcSim = swepc.MonteCarlo(g)
mcFlow = mcSim.initialFlows(ic, bc, iterations=1)

_, axarr = plt.subplots(2, sharex=True, figsize=(8,6))

c = 0
t = 0.0
plotMC()

while t < endTime:
    #pcSim.timestep(pcFlow, dx, dt)
    mcSim.timestep(mcFlow, dx, dt)
    t = t + dt
    c = c + 1
    if c % 4 == 0:
        plotMC()

plt.show(block=True)
