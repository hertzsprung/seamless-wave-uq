import numpy as np
import numpy.polynomial.hermite_e as hermite_e

class GaussianHermiteBasis:
    def __init__(self, degree):
        self.degree = degree
        self.polynomials = [hermite_e.HermiteE.basis(d)
                for d in range(degree+1)]

        self.squareNorm = []
        for d in range(degree+1):
            points, weights = self.quadrature(1+2*d)

            self.squareNorm.append(np.sum([w*self.polynomials[d](xi)**2
                    for xi, w in zip(points, weights)]))

        self.tripleNorm = np.empty((degree+1, degree+1, degree+1))

        points, weights = self.quadrature(1+3*degree)

        for i in range(degree+1):
            for j in range(degree+1):
                for k in range(degree+1):
                    self.tripleNorm[i,j,k] = np.sum(
                            [w*self.polynomials[i](xi)*
                                self.polynomials[j](xi)*
                                self.polynomials[k](xi)
                            for xi, w in zip(points, weights)])

    def __call__(self, xi, coefficients):
        return hermite_e.hermeval(xi, coefficients)

    def quadrature(self, points):
        xi, w = hermite_e.hermegauss(points)
        w /= np.sqrt(2*np.pi)
        return xi, w

    def polynomialOf(self, degree):
        return self.polynomials[degree]

