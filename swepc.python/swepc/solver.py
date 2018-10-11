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

class WellBalancedHSolver:
    def __init__(self, g):
        self.g = g
        self.deterministicFlux = swepc.DeterministicFluxH(g)
        self.sourceTerm = swepc.WellBalancedH()
        self.flowValueClass = swepc.FlowValueH
        self.water = "h"

    def elevationToWater(self, elevation, z):
        return elevation - z

class CentredDifferenceHSolver:
    def __init__(self, g):
        self.g = g
        self.deterministicFlux = swepc.DeterministicFluxH(g)
        self.sourceTerm = swepc.CentredDifference()
        self.flowValueClass = swepc.FlowValueH
        self.water = "h"

    def elevationToWater(self, elevation, z):
        return elevation - z
