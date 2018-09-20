import swepc
import numpy as np
import collections
import multiprocessing as mp

class MonteCarlo:
    def __init__(self, g, sourceTerm, deterministicFlux, flowValueClass):
        self.flowValueClass = flowValueClass
        self.basis = swepc.GaussianHermiteBasis(degree=0)
        riemannSolver = swepc.Roe(deterministicFlux, g)
        riemannEnsemble = swepc.RiemannEnsemble(self.basis, riemannSolver,
                quadraturePoints=1)
        flux = swepc.StochasticFlux(self.basis, riemannEnsemble, sourceTerm)
        self.deterministic = swepc.Simulation(g, flux, sourceTerm)
        self.pool = mp.Pool()

    def initialFlows(self, initialConditions, boundaryConditions,
            topographyGenerator, iterations):
        return MonteCarloFlows(
                self.basis, initialConditions, boundaryConditions,
                self.flowValueClass, topographyGenerator, iterations)

    def timestep(self, flows, dx, dt):
        flows[:] = self.pool.map(MonteCarloTimestep(self.deterministic, dx, dt), flows)

class MonteCarloTimestep:
    def __init__(self, simulation, dx, dt):
        self.simulation = simulation
        self.dx = dx
        self.dt = dt

    def __call__(self, flow):
        return self.simulation.timestep(flow, self.dx, self.dt)

class MonteCarloFlows(collections.Sequence):
    def __init__(self, basis, initialConditions, boundaryConditions,
            flowValueClass, topographyGenerator, iterations):
        self.elements = initialConditions.elements

        self.flows = np.empty(iterations, dtype=swepc.Flow)
        for it in range(iterations):
            ic = swepc.InitialConditions(initialConditions.elements, degree=1)
            for i in range(ic.elements):
                ic.water[i,0] = max(1e-4, np.random.normal(
                        initialConditions.water[i,0],
                        initialConditions.water[i,1]))

                ic.q[i,0] = np.random.normal(
                        initialConditions.q[i,0],
                        initialConditions.q[i,1])

            ic.z[:,0] = topographyGenerator.sample()

            self.flows[it] = swepc.Flow(basis, ic, boundaryConditions,
                    flowValueClass)

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
