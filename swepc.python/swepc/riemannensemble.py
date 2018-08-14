import numpy as np

class RiemannEnsemble:
    def __init__(self, basis, solver, quadraturePoints):
        self.basis = basis
        self.solver = solver
        self.points, self.weights = basis.quadrature(quadraturePoints)

    def integrate(self, left, right, polynomial):
        return np.sum([w / np.sqrt(2*np.pi) * self.solver.flux(left(xi), right(xi)) * 
            polynomial(xi)
            for xi, w in zip(self.points, self.weights)])
