import numpy as np

class Flow:
    def __init__(self, basis, initialConditions, boundaryConditions,
            flowValueClass):
        self.elements = initialConditions.elements
        self.basis = basis
        self.flowValueClass = flowValueClass

        self.water = np.zeros((self.elements, basis.degree+1))
        self.q = np.zeros((self.elements, basis.degree+1))
        self.z = np.zeros((self.elements, basis.degree+1))
        self.zFace = np.zeros((self.elements+1, basis.degree+1))

        degree = min(initialConditions.degree, basis.degree)
        self.water[:,:degree+1] = initialConditions.water[:,:degree+1]
        self.q[:,:degree+1] = initialConditions.q[:,:degree+1]
        self.z[:,:degree+1] = initialConditions.z[:,:degree+1]

        self.zFace[0, :] = self.z[0]
        self.zFace[-1, :] = self.z[-1]
        self.zFace[1:-1, :] = [0.5*(l+r) for l, r in zip(self.z[:], self.z[1:,:])]

        self.upstream_water = self.__applyBC(boundaryConditions.upstream_water, degree)
        self.upstream_q = self.__applyBC(boundaryConditions.upstream_q, degree)
        self.downstream_water = self.__applyBC(boundaryConditions.downstream_water, degree)
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

        return FlowCoeffs(self.water[i], self.q[i], self.z[i],
                self.basis, self.flowValueClass)

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

        left = FlowCoeffs(self.water[leftI], self.q[leftI], self.z[leftI],
                self.basis, self.flowValueClass)
        right = FlowCoeffs(self.water[rightI], self.q[rightI], self.z[rightI],
                self.basis, self.flowValueClass)

        if i == 0:
            if self.upstream_water is not None:
                left.water = self.upstream_water
            if self.upstream_q is not None:
                left.q = self.upstream_q

        if i == self.elements:
            if self.downstream_water is not None:
                right.water = self.downstream_water
            if self.downstream_q is not None:
                left.q = self.downstream_q

        return left, right

    def topographyAtFacesOfElement(self, i):
        return self.zFace[i], self.zFace[i+1]

    def update(self, i, l, increment):
        self.water[i,l] = self.water[i,l] + increment[0]
        self.q[i,l] = self.q[i,l] + increment[1]

class FlowCoeffs:
    def __init__(self, water, q, z, basis, flowValueClass):
        self.water = water
        self.q = q
        self.z = z
        self.basis = basis
        self.flowValueClass = flowValueClass

    def deterministic(self):
        return self.flowValueClass(self.water[0], self.q[0], self.z[0])

    def __call__(self, xi):
        return self.flowValueClass(
                self.basis(xi, self.water),
                self.basis(xi, self.q),
                self.basis(xi, self.z))

class FlowValueEta:
    def __init__(self, eta, q, z):
        self.eta = eta
        self.q = q
        self.z = z

        self.h = self.eta - self.z
        self.__c = None

    def u(self):
        return self.q / self.h

    def c(self, g):
        if self.__c is None:
            self.__c = np.sqrt(g*self.h)

        return self.__c

    def __str__(self):
        return "FlowValueEta<η={eta},q={q},z={z}>".format(eta=self.eta, q=self.q, z=self.z)

    __repr__ = __str__

class FlowValueH:
    def __init__(self, h, q, z):
        self.h = h
        self.q = q
        self.z = z

    def u(self):
        return self.q / self.h

    def c(self, g):
        return np.sqrt(g*self.h)

    def __str__(self):
        return "FlowValueH<h={h},q={q},z={z}>".format(h=self.h, q=self.q, z=self.z)

    __repr__ = __str__

class FlowIncrement:
    @staticmethod
    def array(U0, U1):
        return np.array([U0, U1])

