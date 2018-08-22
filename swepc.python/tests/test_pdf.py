import numpy as np
import swepc
import matplotlib.pyplot as plt

if __name__ == '__main__':
    basis = swepc.GaussianHermiteBasis(degree=3)
    u = np.linspace(-10.0, 10.0, 500)
    coeffs = [1.0, 3.0, -0.3, 0.5]

    plt.plot(u, swepc.PDF(basis)(u, coeffs))
    plt.show()
