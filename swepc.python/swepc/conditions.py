import numpy as np

class InitialConditions:
    def __init__(self, elements, degree):
        self.elements = elements
        self.degree = degree
        self.h = np.zeros((elements, degree+1))
        self.q = np.zeros((elements, degree+1))
        self.z = np.zeros((elements, degree+1))

class BoundaryConditions:
    def __init__(self):
        self.upstream_h = None
        self.upstream_q = None
        self.downstream_h = None
        self.downstream_q = None
