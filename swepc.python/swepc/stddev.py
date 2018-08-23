import numpy as np

class Stddev:
    def __init__(self, flow):
        self.h = np.zeros(flow.elements)
        self.q = np.zeros(flow.elements)
        self.z = np.zeros(flow.elements)

        for i in range(flow.elements):
            for l in range(1, flow.basis.degree+1):
                self.h[i] += flow.h[i,l]**2*flow.basis.squareNorm[l]
                self.q[i] += flow.q[i,l]**2*flow.basis.squareNorm[l]
                self.z[i] += flow.z[i,l]**2*flow.basis.squareNorm[l]

        self.h = np.sqrt(self.h)
        self.q = np.sqrt(self.q)
        self.z = np.sqrt(self.z)