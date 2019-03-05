import numpy as np

class Mesh:
    def __init__(self, domain, elements):
        self.domain = domain
        self.elements = elements
        self.dx = (domain[1] - domain[0])/elements
        self.C = np.linspace(domain[0]+self.dx/2, domain[1]-self.dx/2, elements)
        self.Cf = np.linspace(domain[0], domain[1], elements+1)
