import swepc

class DeterministicFluxEta:
    def __init__(self, g):
        self.g = g

    def __call__(self, flowValue):
        U = flowValue
        return swepc.FlowIncrement.array(U.q, U.q**2/(U.eta - U.z) + 0.5*self.g*(U.eta**2 - 2*U.eta*U.z))

class DeterministicFluxH:
    def __init__(self, g):
        self.g = g

    def __call__(self, flowValue):
        U = flowValue
        return swepc.FlowIncrement.array(U.q, U.q**2/U.h + 0.5*self.g*U.h**2)
