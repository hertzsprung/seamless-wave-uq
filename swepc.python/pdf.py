#!/usr/bin/env python3
import numpy as np
import numpy.polynomial.hermite_e as hermite_e
import matplotlib.pyplot as plt

u_coeffs = np.array([1.0, 3.0, -0.3, 0.5]) # mean, stddev, skew, kurtosis

hermite = hermite_e.HermiteE(u_coeffs)
hermite_prime = hermite.deriv()

def xi_hats(u):
    poly = -hermite_e.herme2poly(hermite.coef)
    poly = np.concatenate(([poly[0] + u], poly[1:]))

    # np.roots() expects array in reverse order (highest degree first)
    return [root for root in np.roots(np.flip(poly)) if np.isreal(root)]

W = lambda xi: hermite_e.hermeweight(xi) / np.sqrt(2.0*np.pi)

def pdf(u):
    return np.sum([1/np.abs(hermite_prime(xi_hat))*W(xi_hat)
        for xi_hat in xi_hats(u)])

def ref_gaussian(u):
    mean = u_coeffs[0]
    stddev = u_coeffs[1]
    return 1/(np.abs(stddev)*np.sqrt(2.0*np.pi)) * np.exp(-((u-mean)/stddev)**2/2)

def ref_secondorder(u):
    mean = u_coeffs[0]
    stddev = u_coeffs[1]
    skew = u_coeffs[2]

    return (np.exp(-(stddev - np.sqrt(stddev**2 + 4*skew * (u - mean + skew)))**2/(8*skew**2)) + \
            np.exp(-(stddev + np.sqrt(stddev**2 + 4*skew * (u - mean + skew)))**2/(8*skew**2))) \
            / (np.sqrt(2*np.pi*np.abs(stddev**2 + 4*skew*(u-mean+skew))))

x = np.linspace(-10.0, 10.0, 500)

plt.plot(x, np.vectorize(pdf)(x))
#plt.plot(x, np.vectorize(ref_gaussian)(x))
#plt.plot(x, np.vectorize(ref_secondorder)(x))
plt.show()
