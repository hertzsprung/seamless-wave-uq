import numpy as np
import numpy.polynomial.hermite_e as hermite_e

class GaussianHermiteBasis:
    def __init__(self, degree):
        self.degree = degree
        self.polynomials = [hermite_e.HermiteE.basis(d)
                for d in range(degree+1)]
        self.weightFunction = lambda xi: 1/np.sqrt(2*np.pi) * np.exp(-xi**2/2)

    def __call__(self, xi, coefficients):
        return hermite_e.hermeval(xi, coefficients)

    def quadrature(self, points):
        return hermite_e.hermegauss(points)

    def ensembleSquareOf(self, degree):
        return [1, 1, 2, 6, 24][degree]

    def polynomialOf(self, degree):
        return self.polynomials[degree]

