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

        self.quadNorm = np.empty((degree+1, degree+1, degree+1, degree+1))

        points, weights = self.quadrature(1+4*degree)

        for i in range(degree+1):
            for j in range(degree+1):
                for k in range(degree+1):
                    for l in range(degree+1):
                        self.quadNorm[i,j,k,l] = np.sum(
                                [w*self.polynomials[i](xi)*
                                    self.polynomials[j](xi)*
                                    self.polynomials[k](xi)*
                                    self.polynomials[l](xi)
                                for xi, w in zip(points, weights)])

    def __call__(self, xi, coefficients):
        return hermite_e.hermeval(xi, coefficients)

    def quadrature(self, points):
        xi, w = hermite_e.hermegauss(points)
        w /= np.sqrt(2*np.pi)
        return xi, w

    def pdf(self, xi):
        return hermite_e.hermeweight(xi) / np.sqrt(2.0*np.pi)

    def polynomialOf(self, degree):
        return self.polynomials[degree]

    def dot(self, coeffs):
        return hermite_e.HermiteE(coeffs)

    def toPolynomial(self, projection):
        return hermite_e.herme2poly(projection.coef)

    def moments(self, coefficients):
        m = np.zeros(4)

        m[0] = coefficients[0]
        mu2 = np.sum([coefficients[p]**2*self.squareNorm[p] for p in range(self.degree+1)])
        m[1] = np.sqrt(np.sum([coefficients[p]**2*self.squareNorm[p] for p in range(1,self.degree+1)]))

        tripleProduct = 0.0
        for i in range(self.degree):
            for j in range(self.degree):
                for k in range(self.degree):
                    tripleProduct += \
                            coefficients[i]*coefficients[j]*coefficients[k]* \
                            self.tripleNorm[i,j,k]

        if m[1] < 1e-12:
            m[2] = 0.0
        else:
            m[2] = m[1]**(-3)*(tripleProduct - 3*m[0]*mu2 + 2*m[0]**3)

        quadProduct = 0.0
        for i in range(self.degree):
            for j in range(self.degree):
                for k in range(self.degree):
                    for l in range(self.degree):
                        quadProduct += \
                                coefficients[i]*coefficients[j]* \
                                coefficients[k]*coefficients[l]* \
                                self.quadNorm[i,j,k,l]

        if m[1] < 1e-12:
            m[3] = 0.0
        else:
            m[3] = m[1]**(-1)*(quadProduct - 4*m[0]*tripleProduct +
                6*m[0]**2*mu2 - 3*m[0]**4)

        return m
