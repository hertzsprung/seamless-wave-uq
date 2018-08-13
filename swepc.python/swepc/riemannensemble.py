import numpy as np
import numpy.polynomial.hermite_e as hermite_e

class RiemannEnsemble:
    def __init__(self, basis, solver, quadraturePoints):
        self.basis = basis
        self.solver = solver
        self.points, self.weights = basis.quadrature(quadraturePoints)

    def integrate(self, left, right, polynomial):
        for xi, w in zip(self.points, self.weights):
            print()
            print(xi, w) 
            print(self.basis.weightFunction(xi) * w)
            print(self.basis.weightFunction(xi) * w * polynomial(xi))
            print(left(xi), right(xi))
            print(self.solver.flux(left(xi), right(xi)))
        print("===")

        print([w * self.solver.flux(left(xi), right(xi)) * 
            polynomial(xi) * self.basis.weightFunction(xi)
            for xi, w in zip(self.points, self.weights)])

        return np.sum([w * self.solver.flux(left(xi), right(xi)) * 
            polynomial(xi) * self.basis.weightFunction(xi)
            for xi, w in zip(self.points, self.weights)], axis=0)
