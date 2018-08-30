import swepc

class DeterministicFlux:
    def __init__(self, g):
        self.g = g

    def __call__(self, flowValue):
        u = flowValue
        return swepc.DynamicFlowValue(u.q, u.q**2/u.h + 0.5*self.g*u.h**2)

