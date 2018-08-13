import numpy as np
import numpy.polynomial.hermite_e as hermite_e

class GaussianHermiteBasis:
    def __init__(self, degree):
        self.degree = degree
        self.weightFunction = lambda xi: 1/np.sqrt(2*np.pi) * np.exp(-xi**2/2)

    def __call__(self, xi, coefficients):
        return hermite_e.hermeval(xi, coefficients)

    def quadrature(self, points):
        return hermite_e.hermegauss(points)

    @classmethod
    def polynomialOf(cls, degree):
        return hermite_e.HermiteE.basis(degree)

