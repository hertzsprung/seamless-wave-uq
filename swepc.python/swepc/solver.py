import numpy as np
import swepc

class WellBalancedEtaSolver:
    def __init__(self, g):
        self.g = g
        self.deterministicFlux = swepc.DeterministicFluxEta(g)
        self.sourceTerm = swepc.WellBalancedEta()
        self.flowValueClass = swepc.FlowValueEta
        self.water = "η"

    def elevationToWater(self, elevation, z):
        return elevation

    def writeDerivedStochasticGalerkinStatistics(self, mesh, flow, file):
        pass
    
    def writeDerivedMonteCarloStatistics(self, mesh, flows, stats, file):
        pass

class HSolver:
    def __init__(self, g):
        self.g = g
        self.deterministicFlux = swepc.DeterministicFluxH(g)
        self.flowValueClass = swepc.FlowValueH
        self.water = "h"

    def elevationToWater(self, elevation, z):
        return elevation - z

    def writeDerivedStochasticGalerkinStatistics(self, mesh, flow, file):
        print("# x mean_eta sigma_eta mean_u sigma_u", file=file)

        for i in range(flow.elements):
            print(mesh.C[i], end=' ', file=file)
            print(flow.z[i,0] + flow.water[i,0], end=' ', file=file)
            print(self.__stddev_eta(flow.z[i,:], flow.water[i,:], flow.basis),
                    end=' ', file=file)
            mean_u = self.__mean_u(flow.atElement(i), flow.basis)
            print(mean_u, end=' ', file=file)
            print(self.__stddev_u(flow.atElement(i), mean_u, flow.basis),
                    file=file)

    def __stddev_eta(self, z, h, basis):
        return np.sqrt(np.sum([(h[p] + z[p])**2*basis.squareNorm[p]
            for p in range(1, basis.degree+1)]))

    def __mean_u(self, flow, basis):
        xis = np.linspace(-5.0, 5.0, 128)
        ws = [basis.pdf(xi) for xi in xis]
        return np.sum([w*flow(xi).q/flow(xi).h for xi, w in zip(xis, ws)])/np.sum(ws)

    def __stddev_u(self, flow, mean_u, basis):
        xis = np.linspace(-5.0, 5.0, 128)
        ws = [basis.pdf(xi) for xi in xis]
        return np.sqrt(np.sum([w*(flow(xi).q/flow(xi).h - mean_u)**2
            for xi, w in zip(xis, ws)])/np.sum(ws))
    
    def writeDerivedMonteCarloStatistics(self, mesh, flows, stats, file):
        stddev_eta = np.std([flow.z[:,0] + flow.water[:,0] for flow in flows], axis=0)

        print("# x mean_eta sigma_eta", file=file)
        for i in range(flows.elements):
            print(mesh.C[i], end=' ', file=file)
            print(stats.z[i,0] + stats.water[i,0], end=' ', file=file)
            print(stddev_eta[i], file=file)

class WellBalancedHSolver(HSolver):
    def __init__(self, g):
        super().__init__(g)
        self.sourceTerm = swepc.WellBalancedH()

class CentredDifferenceHSolver(HSolver):
    def __init__(self, g):
        super().__init__(g)
        self.sourceTerm = swepc.CentredDifference()
