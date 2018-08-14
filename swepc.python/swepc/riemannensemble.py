import numpy as np
import numpy.polynomial.hermite_e as hermite_e

class RiemannEnsemble:
    def __init__(self, basis, solver, quadraturePoints):
        self.basis = basis
        self.solver = solver
        self.points, self.weights = basis.quadrature(quadraturePoints)

    def integrate(self, left, right, polynomial):
        #for xi, w in zip(self.points, self.weights):
        #    print(xi, w*self.basis.weightFunction(xi)*polynomial(xi), left(xi), right(xi))

        return np.sum([w * self.solver.flux(left(xi), right(xi)) * 
            polynomial(xi) * self.basis.weightFunction(xi)
            for xi, w in zip(self.points, self.weights)])
