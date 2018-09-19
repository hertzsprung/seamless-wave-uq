#!/usr/bin/env python3
import swepc
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

def initialisePC(initialConditions, boundaryConditions, sourceTerm,
        deterministicFlux, flowValueClass, degree):
    basis = swepc.GaussianHermiteBasis(degree)
    riemannSolver = swepc.Roe(deterministicFlux, g)
    riemannEnsemble = swepc.RiemannEnsemble(
            basis, riemannSolver, quadraturePoints=degree+1)
    flux = swepc.StochasticFlux(basis, riemannEnsemble, sourceTerm)
    flow = swepc.Flow(basis, initialConditions, boundaryConditions,
            flowValueClass)

    return swepc.Simulation(g, flux, sourceTerm), flow

def plotPC():
    stddev = swepc.Stddev(pcFlow)

    axarr[0].cla()
    axarr[0].set_ylim((0,3))
    axarr[0].fill_between(xCentre,
            pcFlow.z[:,0] - stddev.z,
            pcFlow.z[:,0] + stddev.z, 
            color='lightslategray')
    axarr[0].plot(xCentre, pcFlow.z[:,0], color='k')

#    axarr[0].fill_between(xCentre,
#            pcFlow.water[:,0] - stddev.water,
#            pcFlow.water[:,0] + stddev.water, 
#            color='lightskyblue')
#    axarr[0].plot(xCentre, pcFlow.water[:,0], color='mediumblue')

    axarr[0].fill_between(xCentre,
            pcFlow.z[:,0] + pcFlow.water[:,0] - stddev.water,
            pcFlow.z[:,0] + pcFlow.water[:,0] + stddev.water, 
            color='lightskyblue')
    axarr[0].plot(xCentre, pcFlow.z[:,0] + pcFlow.water[:,0], color='mediumblue')

    axarr[0].annotate("$t$ = {0:.3f}".format(t), (0, 0.9), xycoords='axes fraction')
    axarr[0].annotate("$cfl$ = {0:.3f}".format(
        dt/dx*pcFlowInfo.maxWaveSpeed(pcFlow)), (0, 0.8), xycoords='axes fraction')

    axarr[1].cla()
    #axarr[1].set_ylim((-1e-3,1e-3))
    axarr[1].set_ylabel("q")
    axarr[1].fill_between(xCentre,
            pcFlow.q[:,0] - stddev.q,
            pcFlow.q[:,0] + stddev.q, 
            color='plum')
    axarr[1].plot(xCentre, pcFlow.q[:,0], color='purple')

    plt.draw()
    plt.pause(0.001)
    #plt.savefig("/tmp/sim/{0:06.3f}.png".format(t))

def topography(x):
    z = 0.0

    if 8 < x and x <= 12:
        z = 2.0 - 0.5*pow(x-10, 2)
    elif 22 < x <= 25:
        z = 0.5*x - 11.0
    elif 25 < x <= 28:
        z = -0.5*x + 14.0
    elif 39 < x <= 46:
        z = 3.0

    return z*0.5

np.seterr(invalid='raise', divide='raise')

g = 9.80665
N = 64
domain = [0.0, 50.0]
dx = (domain[1] - domain[0])/N
dt = 0.08
endTime = 50.0

xCentre = np.linspace(dx/2, domain[1]-dx/2, N)
xFace = np.linspace(0, domain[1], N+1)

ic = swepc.InitialConditions(N, degree=1)

zFace = [topography(x) for x in xFace]
ic.z[:,0] = [0.5*(l+r) for l, r in zip(zFace, zFace[1:])]
ic.z[:,1] = [0.8/np.sqrt(2*np.pi)*np.exp(-(1.5*(x-10))**2/2) for x in xCentre]

bc = swepc.BoundaryConditions()

#sourceTerm = swepc.WellBalancedEta()
#deterministicFlux = swepc.DeterministicFluxEta(g)
#flowValueClass = swepc.FlowValueEta
#pcFlowInfo = swepc.FlowInfoEta(g)
#ic.water[:,0] = 2.0

sourceTerm = swepc.WellBalancedH()
deterministicFlux = swepc.DeterministicFluxH(g)
flowValueClass = swepc.FlowValueH
pcFlowInfo = swepc.FlowInfoH(g)
ic.water[:,0] = [2.0 - z for z in ic.z[:,0]]

pcSim, pcFlow = initialisePC(ic, bc, sourceTerm, deterministicFlux,
        flowValueClass, degree=3)

_, axarr = plt.subplots(2, figsize=(6,6))

c = 0
t = 0.0

while t < endTime:
    pcSim.timestep(pcFlow, dx, dt)
    t = t + dt
    c = c + 1
    #if c % 8 == 0:
    plotPC()

plt.show(block=True)
