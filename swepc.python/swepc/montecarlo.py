import numpy as np
import swepc

class MonteCarlo:
    def __init__(self, g):
        self.basis = swepc.GaussianHermiteBasis(degree=0)
        solver = swepc.Roe(g)
        riemannEnsemble = swepc.RiemannEnsemble(self.basis, solver,
                quadraturePoints=1)
        flux = swepc.Flux(self.basis, riemannEnsemble)
        self.deterministic = swepc.Simulation(flux) 

    def simulate(self, stochasticFlow, dx, dt, endTime, iterations):
        samples_h = np.empty((iterations, stochasticFlow.elements))

        for run in range(iterations):
            flow = self.__sample(stochasticFlow, dx, dt, endTime)
            samples_h[run,:] = flow.h[:,0]
            print("# iteration ", run, ", integral(variance)",
                    np.sum(np.var(samples_h[:run+1,:], axis=0)))

        basis = swepc.GaussianHermiteBasis(degree=1)
        result = swepc.Flow(stochasticFlow.elements, basis)
        result.h[:,0] = np.mean(samples_h, axis=0)
        result.h[:,1] = np.std(samples_h, axis=0)

        return result

    def __sample(self, stochasticFlow, dx, dt, endTime):
        flow = swepc.Flow(stochasticFlow.elements, self.basis)
        for i in range(flow.elements):
            flow.h[i,0] = max(1e-4, np.random.normal(
                    stochasticFlow.h[i,0],
                    stochasticFlow.h[i,1]))

            flow.q[i,0] = np.random.normal(
                    stochasticFlow.q[i,0],
                    stochasticFlow.q[i,1])

        t = 0.0
        while t < endTime:
            self.deterministic.timestep(flow, dx, dt)
            t = t + dt

        return flow
