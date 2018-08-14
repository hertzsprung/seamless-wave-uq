import numpy as np
import swepc

class Flux:
    def __init__(self, basis, riemannEnsemble):
        self.basis = basis
        self.riemannEnsemble = riemannEnsemble

    def evaluate(self, flow):
        flux = np.empty((flow.elements+1, self.basis.degree+1),
                dtype=swepc.FlowValue)

        for i in range(flow.elements+1):
            coeffsPlus, coeffsMinus = flow.atFace(i)

            for l in range(self.basis.degree+1):
                flux[i,l] = \
                        self.riemannEnsemble.integrate(coeffsPlus, coeffsMinus,
                        self.basis.polynomialOf(degree=l))

        return flux
