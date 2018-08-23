import numpy as np
import swepc

class PDF:
    def __init__(self, basis):
        self.basis = basis

    def __call__(self, u, coeffs):
        projection = self.basis.dot(coeffs)
        derivative = projection.deriv()

        return [self.__pdf(u_, projection, derivative) for u_ in u]

    def __pdf(self, u, projection, derivative):
        return np.sum([1.0/np.abs(derivative(xi_hat))*self.basis.pdf(xi_hat)
            for xi_hat in self.__xi_hats(projection, u)])

    def __xi_hats(self, projection, u):
        poly = -self.basis.toPolynomial(projection)
        poly = np.concatenate(([poly[0] + u], poly[1:]))

        # np.roots() expects array in reverse order (highest degree first)
        return [np.real(root)
                for root in np.roots(np.flip(poly)) if np.isreal(root)]
