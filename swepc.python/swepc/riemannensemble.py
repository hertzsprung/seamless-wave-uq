import numpy as np

class RiemannEnsemble:
    def __init__(self, basis, riemann, quadraturePoints):
        self.basis = basis
        self.riemann = riemann
        self.points, self.weights = basis.quadrature(quadraturePoints)

    def integrate(self, left, right, polynomial):
        return np.sum([w * self.riemann.flux(left(xi), right(xi)) * 
            polynomial(xi)
            for xi, w in zip(self.points, self.weights)], axis=0)

class DeterministicRiemannEnsemble:
    def __init__(self, riemann):
        self.riemann = riemann

    def integrate(self, left, right, polynomial):
        return self.riemann.flux(left.deterministic(), right.deterministic())
