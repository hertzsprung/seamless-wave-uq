import swepc
import numpy as np
import collections

class MonteCarlo:
    def __init__(self, g, sourceTerm, deterministicFlux, flowValueClass):
        self.flowValueClass = flowValueClass
        self.basis = swepc.GaussianHermiteBasis(degree=0)
        riemannSolver = swepc.Roe(deterministicFlux, g)
        riemannEnsemble = swepc.RiemannEnsemble(self.basis, riemannSolver,
                quadraturePoints=1)
        flux = swepc.StochasticFlux(self.basis, riemannEnsemble, sourceTerm)
        self.deterministic = swepc.Simulation(g, flux, sourceTerm)

    def simulate(self, initialConditions, boundaryConditions,
            topographyGenerator, dx, dt, endTime, iterations,
            convergenceSampleIndex):
        flows = MonteCarloFlows(initialConditions)
        oldSampleStats = np.array([0.0, 0.0])

        for i in range(iterations):
            flow = self.__randomisedFlow(initialConditions, boundaryConditions,
                    topographyGenerator)
            flows.append(self.__simulateDeterministic(flow, dx, dt, endTime))
            stats = MonteCarloFlowStatistics(flows)
            sampleStats = stats.water[convergenceSampleIndex,:]
            sampleStatsDiff = np.abs(sampleStats - oldSampleStats)
            print(len(flows), sampleStatsDiff[0], sampleStatsDiff[1])
            oldSampleStats = sampleStats

    def __randomisedFlow(self, initialConditions, boundaryConditions,
            topographyGenerator):
        ic = swepc.InitialConditions(initialConditions.elements,
                degree=1)
        for i in range(ic.elements):
            ic.water[i,0] = max(1e-4, np.random.normal(
                    initialConditions.water[i,0],
                    initialConditions.water[i,1]))

            ic.q[i,0] = np.random.normal(
                    initialConditions.q[i,0],
                    initialConditions.q[i,1])

        ic.z[:,0] = topographyGenerator.sample()

        return swepc.Flow(self.basis, ic, boundaryConditions,
                self.flowValueClass)

    def __simulateDeterministic(self, flow, dx, dt, endTime):
        t = 0.0
        while t < endTime:
            t = t + dt
            flow = self.deterministic.timestep(flow, dx, dt)
        return flow

class MonteCarloFlows(collections.Sequence):
    def __init__(self, initialConditions):
         self.elements = initialConditions.elements
         self.flows = []

    def append(self, flow):
        self.flows.append(flow)

    def __getitem__(self, index):
        return self.flows[index]

    def __setitem__(self, index, item):
        self.flows[index] = item

    def __len__(self):
        return len(self.flows)

class MonteCarloFlowStatistics:
    def __init__(self, flows):
        self.water = np.zeros((flows.elements, 2))
        self.q = np.zeros((flows.elements, 2))
        self.z = np.zeros((flows.elements, 2))

        self.water[:,0] = np.mean([flow.water[:,0] for flow in flows], axis=0)
        self.q[:,0] = np.mean([flow.q[:,0] for flow in flows], axis=0)
        self.z[:,0] = np.mean([flow.z[:,0] for flow in flows], axis=0)
        self.water[:,1] = np.std([flow.water[:,0] for flow in flows], axis=0)
        self.q[:,1] = np.std([flow.q[:,0] for flow in flows], axis=0)
        self.z[:,1] = np.std([flow.z[:,0] for flow in flows], axis=0)
