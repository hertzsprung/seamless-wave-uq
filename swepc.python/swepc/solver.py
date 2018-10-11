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

    def writeDerivedStatistics(self, mesh, flow, stats, file):
        pass

class HSolver:
    def __init__(self, g):
        self.g = g
        self.deterministicFlux = swepc.DeterministicFluxH(g)
        self.flowValueClass = swepc.FlowValueH
        self.water = "h"

    def elevationToWater(self, elevation, z):
        return elevation - z

    def writeDerivedStatistics(self, mesh, flow, stats, file):
        print("# x mean_eta sigma_eta", file=file)

        for i in range(flow.elements):
            print(mesh.C[i], end=' ', file=file)
            print(flow.z[i,0] + flow.water[i,0], end=' ', file=file)
            print(self.__stddev_eta(flow.z[i,:], flow.water[i,:], flow.basis),
                    file=file)

    def __stddev_eta(self, z,h , basis):
        return np.sqrt(np.sum([(h[p] + z[p])**2*basis.squareNorm[p]
            for p in range(1, basis.degree+1)]))

class WellBalancedHSolver(HSolver):
    def __init__(self, g):
        super().__init__(g)
        self.sourceTerm = swepc.WellBalancedH()

class CentredDifferenceHSolver(HSolver):
    def __init__(self, g):
        super().__init__(g)
        self.sourceTerm = swepc.CentredDifference()
