import numpy as np

class Flow:
    def __init__(self, elements, basis):
        self.h = np.zeros((elements, basis.degree+1))
        self.q = np.zeros((elements, basis.degree+1))
        self.z = np.zeros((elements+1, basis.degree+1))
        self.elements = elements
        self.basis = basis
        self.upstream_q = None
        self.downstream_h = None

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

        left = FlowCoeffs(self.h[leftI], self.q[leftI], self.basis)
        right = FlowCoeffs(self.h[rightI], self.q[rightI], self.basis)

        if i == 0:
            if self.upstream_q is not None:
                left.q = self.upstream_q

        if i == self.elements:
            if self.downstream_h is not None:
                right.h = self.downstream_h

        return left, right

    def update(self, i, l, increment):
        self.h[i,l] = self.h[i,l] + increment.h
        self.q[i,l] = self.q[i,l] + increment.q

    def maxWaveSpeed(self, g):
        v = 0.0
        for i in range(self.elements):
            v = max(v, abs(self.q[i,0] / self.h[i,0]) + np.sqrt(g*self.h[i,0]))
        return v

    def variance(self):
        var = np.empty(self.elements, dtype=FlowValue)

        for i in range(self.elements):
            var[i] = FlowValue(0.0, 0.0)

            for l in range(1, self.basis.degree+1):
                var[i].h += self.h[i,l]**2*self.basis.squareNorm[l]
                var[i].q += self.q[i,l]**2*self.basis.squareNorm[l]

        return var

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
