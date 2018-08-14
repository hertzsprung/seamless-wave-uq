import numpy as np

class Flow:
    def __init__(self, elements, basis):
        self.h = np.zeros((elements, basis.degree+1))
        self.q = np.zeros((elements, basis.degree+1))
        self.elements = elements
        self.basis = basis

    def atFace(self, i):
        if i == 0:
            leftI = i
            rightI = i
        elif i == self.elements:
            leftI = i-1
            rightI = i-1
        else:
            leftI = i-1
            rightI = i

        return FlowCoeffs(self.h[leftI], self.q[leftI], self.basis), \
                FlowCoeffs(self.h[rightI], self.q[rightI], self.basis)

    def update(self, i, l, increment):
        self.h[i,l] = self.h[i,l] + increment.h
        self.q[i,l] = self.q[i,l] + increment.q

    def maxWaveSpeed(self, g):
        v = 0.0
        for i in range(self.elements):
            v = max(v, abs(self.q[i,0] / self.h[i,0]) + np.sqrt(g*self.h[i,0]))
        return v

class FlowCoeffs:
    def __init__(self, h, q, basis):
        self.h = h
        self.q = q
        self.basis = basis

    def __call__(self, xi):
        return FlowValue(self.basis(xi, self.h), self.basis(xi, self.q))

class FlowValue:
    def __init__(self, h, q):
        self.h = h
        self.q = q

    def flux(self, g):
        return FlowValue(h=self.q, q=self.q**2/self.h + 0.5*g*self.h**2)

    @classmethod
    def fromarray(cls, array):
        return cls(array[0], array[1])

    def u(self):
        return self.q / self.h

    def c(self, g):
        return np.sqrt(g*self.h)

    def __add__(self, other):
        return FlowValue(self.h+other.h, self.q+other.q)

    def __sub__(self, other):
        return FlowValue(self.h-other.h, self.q-other.q)

    def __mul__(self, scalar):
        return FlowValue(scalar*self.h, scalar*self.q)
    
    def __rmul__(self, scalar):
        return FlowValue(scalar*self.h, scalar*self.q)

    def __str__(self):
        return "FlowValue<h={h},q={q}>".format(h=self.h, q=self.q)

    __repr__ = __str__
