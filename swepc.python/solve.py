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
    axarr[0].set_ylim((0,2.5))
    axarr[0].fill_between(xCentre,
            pcFlow.z[:,0] - stddev.z,
            pcFlow.z[:,0] + stddev.z, 
            color='lightslategray')
    axarr[0].plot(xCentre, pcFlow.z[:,0], color='k')

    axarr[0].fill_between(xCentre,
            pcFlow.water[:,0] - stddev.water,
            pcFlow.water[:,0] + stddev.water, 
            color='lightskyblue')
    axarr[0].plot(xCentre, pcFlow.water[:,0], color='mediumblue')

#    axarr[0].fill_between(xCentre,
#            pcFlow.z[:,0] + pcFlow.water[:,0] - stddev.water,
#            pcFlow.z[:,0] + pcFlow.water[:,0] + stddev.water, 
#            color='lightskyblue')
#    axarr[0].plot(xCentre, pcFlow.z[:,0] + pcFlow.water[:,0], color='mediumblue')

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

class Bump:
    def __init__(self, a_mean, a_stddev, halfWidth):
        self.a_mean = a_mean
        self.a_stddev = a_stddev
        self.halfWidth = np.pi/halfWidth

    def z0(self, x):
        return self.a_mean*(1/np.cosh(self.halfWidth*x))**2

    def z1(self, x):
        return np.sqrt(self.__dzda(x)**2 * self.a_stddev**2)

    def __dzda(self, x):
        return self.halfWidth*x \
                * np.tanh(self.halfWidth*x) \
                * (1/np.cosh(self.halfWidth*x))**2 \
                - (1/np.cosh(self.halfWidth*x))**2

class TwoBumps:
    def __init__(self, a_mean, a_stddev, halfWidth):
        self.a_mean = a_mean
        self.a_stddev = a_stddev
        self.halfWidth = np.pi/halfWidth

    def z0(self, x):
        z = 0.0

        #if -40 < x and x <= -35:
        #    z = (self.a_mean/5)*x + 8*self.a_mean
        #elif -35 < x and x <= -30:
        #    z = -(self.a_mean/5)*x - 6*self.a_mean
        if 30 < x and x <= 40:
            z = self.a_mean

        return z + self.a_mean*(1/np.cosh(self.halfWidth*x))**2

    def z1(self, x):
        return np.sqrt(self.__dzda(x)**2 * self.a_stddev**2)

    def __dzda(self, x):
        return self.halfWidth*x \
                * np.tanh(self.halfWidth*x) \
                * (1/np.cosh(self.halfWidth*x))**2 \
                - (1/np.cosh(self.halfWidth*x))**2


np.seterr(invalid='raise', divide='raise')

g = 9.80665
N = 200
domain = [-50.0, 50.0]
dx = (domain[1] - domain[0])/N
dt = 0.08
endTime = 500.0

xCentre = np.linspace(domain[0]+dx/2, domain[1]-dx/2, N)

ic = swepc.InitialConditions(N, degree=1)

bump = TwoBumps(a_mean=0.8, a_stddev=0.16, halfWidth=10.0)

ic.z[:,0] = [bump.z0(x) for x in xCentre]
ic.z[:,1] = [bump.z1(x) for x in xCentre]

bc = swepc.BoundaryConditions()
#bc.upstream_q = [1.125, 0.0]
#bc.downstream_water = [1.5, 0.0]

sourceTerm = swepc.WellBalancedEta()
#sourceTerm = swepc.CentredDifference()
deterministicFlux = swepc.DeterministicFluxEta(g)
flowValueClass = swepc.FlowValueEta
pcFlowInfo = swepc.FlowInfoEta(g)
ic.water[:,0] = 1.5

#sourceTerm = swepc.WellBalancedH()
#deterministicFlux = swepc.DeterministicFluxH(g)
#flowValueClass = swepc.FlowValueH
#pcFlowInfo = swepc.FlowInfoH(g)
#ic.water[:,0] = [1.0 - z for z in ic.z[:,0]]

pcSim, pcFlow = initialisePC(ic, bc, sourceTerm, deterministicFlux,
        flowValueClass, degree=3)

convergence = swepc.Convergence(pcFlow)

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
