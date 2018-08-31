import numpy as np

class Flow:
    def __init__(self, basis, initialConditions, boundaryConditions):
        self.elements = initialConditions.elements
        self.basis = basis

        self.eta = np.zeros((self.elements, basis.degree+1))
        self.q = np.zeros((self.elements, basis.degree+1))
        self.z = np.zeros((self.elements, basis.degree+1))
        self.zFace = np.zeros((self.elements+1, basis.degree+1))

        degree = min(initialConditions.degree, basis.degree)
        self.eta[:,:degree+1] = initialConditions.eta[:,:degree+1]
        self.q[:,:degree+1] = initialConditions.q[:,:degree+1]
        self.z[:,:degree+1] = initialConditions.z[:,:degree+1]

        self.zFace[0, :] = self.z[0]
        self.zFace[-1, :] = self.z[-1]
        self.zFace[1:-1, :] = [0.5*(l+r) for l, r in zip(self.z[:], self.z[1:,:])]

        self.upstream_eta = self.__applyBC(boundaryConditions.upstream_eta, degree)
        self.upstream_q = self.__applyBC(boundaryConditions.upstream_q, degree)
        self.downstream_eta = self.__applyBC(boundaryConditions.downstream_eta, degree)
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

        return FlowCoeffs(self.eta[i], self.q[i], self.z[i], self.basis)

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

        left = FlowCoeffs(self.eta[leftI], self.q[leftI], self.z[leftI], self.basis)
        right = FlowCoeffs(self.eta[rightI], self.q[rightI], self.z[rightI], self.basis)

        if i == 0:
            if self.upstream_eta is not None:
                left.h = self.upstream_eta
            if self.upstream_q is not None:
                left.q = self.upstream_q

        if i == self.elements:
            if self.downstream_eta is not None:
                right.h = self.downstream_eta
            if self.downstream_q is not None:
                left.q = self.downstream_q

        return left, right

    def topographyAtFacesOfElement(self, i):
        return self.zFace[i], self.zFace[i+1]

    def update(self, i, l, increment):
        self.eta[i,l] = self.eta[i,l] + increment[0]
        self.q[i,l] = self.q[i,l] + increment[1]

    def maxWaveSpeed(self, g):
        v = 0.0
        for i in range(self.elements):
            h = self.eta[i,0] - self.z[i,0]
            v = max(v, abs(self.q[i,0] / h) + np.sqrt(g*h))
        return v

class FlowCoeffs:
    def __init__(self, eta, q, z, basis):
        self.eta = eta
        self.q = q
        self.z = z
        self.basis = basis

    def __call__(self, xi):
        return FlowValue(
                self.basis(xi, self.eta),
                self.basis(xi, self.q),
                self.basis(xi, self.z))

class FlowValue:
    def __init__(self, eta, q, z):
        self.eta = eta
        self.q = q
        self.z = z

        self.h = self.eta - self.z

    def u(self):
        return self.q / self.h

    def c(self, g):
        return np.sqrt(g*self.h)

    def __str__(self):
        return "FlowValue<η={eta},q={q},z={z}>".format(eta=self.eta, q=self.q, z=self.z)

    __repr__ = __str__

class FlowIncrement:
    @staticmethod
    def array(U0, U1):
        return np.array([U0, U1])

