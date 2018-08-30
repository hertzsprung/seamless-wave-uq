import numpy as np

class Flow:
    def __init__(self, basis, initialConditions, boundaryConditions):
        self.elements = initialConditions.elements
        self.basis = basis

        self.h = np.zeros((self.elements, basis.degree+1))
        self.q = np.zeros((self.elements, basis.degree+1))
        self.z = np.zeros((self.elements, basis.degree+1))
        self.zFace = np.zeros((self.elements+1, basis.degree+1))

        degree = min(initialConditions.degree, basis.degree)
        self.h[:,:degree+1] = initialConditions.h[:,:degree+1]
        self.q[:,:degree+1] = initialConditions.q[:,:degree+1]
        self.z[:,:degree+1] = initialConditions.z[:,:degree+1]

        self.zFace[0, :] = self.z[0]
        self.zFace[-1, :] = self.z[-1]
        self.zFace[1:-1, :] = [0.5*(l+r) for l, r in zip(self.z[:], self.z[1:,:])]

        self.upstream_h = self.__applyBC(boundaryConditions.upstream_h, degree)
        self.upstream_q = self.__applyBC(boundaryConditions.upstream_q, degree)
        self.downstream_h = self.__applyBC(boundaryConditions.downstream_h, degree)
        self.downstream_q = self.__applyBC(boundaryConditions.downstream_q, degree)

    def __applyBC(self, source, degree):
        if source is not None:
            target = np.zeros(self.basis.degree+1)
            target[:degree+1] = source[:degree+1]
            return target
        else:
            return None

    def atElement(self, i):
        if i < 0:
            i = 0
        elif i >= self.elements:
            i = self.elements-1

        return FlowCoeffs(self.h[i], self.q[i], self.z[i], self.basis)

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

        left = FlowCoeffs(self.h[leftI], self.q[leftI], self.z[leftI], self.basis)
        right = FlowCoeffs(self.h[rightI], self.q[rightI], self.z[rightI], self.basis)

        if i == 0:
            if self.upstream_h is not None:
                left.h = self.upstream_h
            if self.upstream_q is not None:
                left.q = self.upstream_q

        if i == self.elements:
            if self.downstream_h is not None:
                right.h = self.downstream_h
            if self.downstream_q is not None:
                left.q = self.downstream_q

        return left, right

    def topographyAtFacesOfElement(self, i):
        return self.zFace[i], self.zFace[i+1]

    def update(self, i, l, increment):
        self.h[i,l] = self.h[i,l] + increment.h
        self.q[i,l] = self.q[i,l] + increment.q

    def maxWaveSpeed(self, g):
        v = 0.0
        for i in range(self.elements):
            v = max(v, abs(self.q[i,0] / self.h[i,0]) + np.sqrt(g*self.h[i,0]))
        return v

class FlowCoeffs:
    def __init__(self, h, q, z, basis):
        self.h = h
        self.q = q
        self.z = z
        self.basis = basis

    def __call__(self, xi):
        return FlowValue(
                self.basis(xi, self.h),
                self.basis(xi, self.q),
                self.basis(xi, self.z))

class FlowValue:
    def __init__(self, h, q, z):
        self.h = h
        self.q = q
        self.z = z

    def u(self):
        return self.q / self.h

    def c(self, g):
        return np.sqrt(g*self.h)

class DynamicFlowValue:
    def __init__(self, h, q):
        self.h = h
        self.q = q

    def u(self):
        return self.q / self.h

    def c(self, g):
        return np.sqrt(g*self.h)

    @classmethod
    def fromarray(cls, array):
        return cls(array[0], array[1])

    def __add__(self, other):
        return DynamicFlowValue(self.h+other.h, self.q+other.q)

    def __sub__(self, other):
        return DynamicFlowValue(self.h-other.h, self.q-other.q)

    def __mul__(self, scalar):
        return DynamicFlowValue(scalar*self.h, scalar*self.q)
    
    def __rmul__(self, scalar):
        return DynamicFlowValue(scalar*self.h, scalar*self.q)

    def __str__(self):
        return "DynamicFlowValue<{h},{q}>".format(h=self.h, q=self.q)

    __repr__ = __str__
