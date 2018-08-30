#!/usr/bin/env python3
import swepc
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

def intrusivePC(initialConditions, boundaryConditions, sourceTerm, degree):
    basis = swepc.GaussianHermiteBasis(degree)
    riemannSolver = swepc.Roe(swepc.DeterministicFlux(g), g)
    riemannEnsemble = swepc.RiemannEnsemble(
            basis, riemannSolver, quadraturePoints=degree+1)
    flux = swepc.StochasticFlux(basis, riemannEnsemble, sourceTerm)
    flow = swepc.Flow(basis, initialConditions, boundaryConditions)

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
    axarr[0].fill_between(xCentre,
            pcFlow.z[:,0] + pcFlow.h[:,0] - stddev.h,
            pcFlow.z[:,0] + pcFlow.h[:,0] + stddev.h, 
            color='lightskyblue')
    axarr[0].plot(xCentre, pcFlow.z[:,0] + pcFlow.h[:,0], color='mediumblue')
    axarr[0].annotate("$t$ = {0:.3f}".format(t), (0, 0.9), xycoords='axes fraction')
    axarr[0].annotate("$cfl$ = {0:.3f}".format(dt/dx*pcFlow.maxWaveSpeed(g)), (0, 0.8), xycoords='axes fraction')

    axarr[1].cla()
    axarr[1].set_ylim((-1e-3,1e-3))
    axarr[1].set_ylabel("q")
    axarr[1].fill_between(xCentre,
            pcFlow.q[:,0] - stddev.q,
            pcFlow.q[:,0] + stddev.q, 
            color='plum')
    axarr[1].plot(xCentre, pcFlow.q[:,0], color='purple')

    #axarr[1].cla()
    #axarr[1].set_xlabel('h')
    #axarr[1].set_title('PDF')
    ## find h mean for element 29, generate a linspace around that
    #hmean29 = pcFlow.h[29,0]
    #hstddev29 = pcFlow.h[29,1]
    #u = np.linspace(0, 3, 100)
    #pdf = swepc.PDF(pcFlow.basis)(u, pcFlow.h[29,:])
    #axarr[1].plot(u, pdf, label='Polynomial Chaos')

    #mcEta29 = [flow.z[29,0] + flow.h[29,0] for flow in mcFlow]
    #sns.kdeplot(mcEta29, ax=axarr[1], label='Monte Carlo')
    #axarr[1].legend(loc=1)

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

    #for flow in mcFlow:
    #    axarr[0].plot(xCentre, flow.z[:,0] + flow.h[:,0], color='lightskyblue', lw=0.5)
    #axarr[0].fill_between(xCentre,
    #        stats.z[:,0] + stats.h[:,0] - stats.h[:,1],
    #        stats.z[:,0] + stats.h[:,0] + stats.h[:,1], 
    #        color='lightskyblue')
    axarr[0].plot(xCentre, stats.z[:,0] + stats.h[:,0], color='mediumblue')
    eta10 = [flow.z[10,0] + flow.h[10,0] for flow in mcFlow]
    eta29 = [flow.z[29,0] + flow.h[29,0] for flow in mcFlow]
    eta54 = [flow.z[54,0] + flow.h[54,0] for flow in mcFlow]
    axarr[0].violinplot([eta10, eta29, eta54], [xCentre[10], xCentre[29], xCentre[54]], widths=3.0)
    axarr[0].text(2, 0.75, "$t$ = {0:.3f}".format(t))

#    axarr[1].cla()
#    axarr[1].set_ylim((4,5))
#    axarr[1].set_ylabel("q")
#    for flow in mcFlow:
#        axarr[1].plot(xCentre, flow.q[:,0], color='plum', lw=0.5)
#    #axarr[1].fill_between(xCentre,
#    #        stats.q[:,0] - stats.q[:,1],
#    #        stats.q[:,0] + stats.q[:,1], 
#    #        color='plum')
#    axarr[1].plot(xCentre, stats.q[:,0], color='purple')
#
#    axarr[2].cla()
#    axarr[2].set_ylim((-0.2,2.5))
#    axarr[2].set_ylabel("Fr")
#    for flow in mcFlow:
#        axarr[2].plot(xCentre, flow.q[:,0]/flow.h[:,0]/np.sqrt(g*flow.h[:,0]), color='C2', lw=0.5)

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
ic.h[:,0] = [2.0 - z for z in ic.z[:,0]]

bc = swepc.BoundaryConditions()

sourceTerm = swepc.WellBalancedH()
#sourceTerm = swepc.CentredDifference()

pcSim, pcFlow = intrusivePC(ic, bc, sourceTerm, degree=3)
mcSim = swepc.MonteCarlo(g, sourceTerm)
mcFlow = mcSim.initialFlows(ic, bc, iterations=50)

_, axarr = plt.subplots(2, figsize=(6,6))
#axarr = [axarr]

c = 0
t = 0.0
#plotMC()

while t < endTime:
    pcSim.timestep(pcFlow, dx, dt)
    #mcSim.timestep(mcFlow, dx, dt)
    t = t + dt
    c = c + 1
    #if c % 8 == 0:
    plotPC()

plt.show(block=True)
