import numpy as np
import swepc

class StochasticFlux:
    def __init__(self, basis, riemannEnsemble, sourceTerm):
        self.basis = basis
        self.riemannEnsemble = riemannEnsemble
        self.sourceTerm = sourceTerm

    def __call__(self, flow):
        flux = np.empty((flow.elements+1, self.basis.degree+1, 2))

        for i in range(flow.elements+1):
            left, right = self.sourceTerm.balancedRiemannInputs(flow, i)

            for l in range(self.basis.degree+1):
                flux[i,l] = \
                        self.riemannEnsemble.integrate(left, right,
                        self.basis.polynomialOf(degree=l))

        return flux
