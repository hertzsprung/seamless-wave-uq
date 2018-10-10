import swepc

class CentredDifference:
    def __call__(self, g, flow, i, l):
        coeffs = flow.atElement(i)
        z_left, z_right = flow.topographyAtFacesOfElement(i)

        q = 0.0

        for p in range(flow.basis.degree+1):
            for p_prime in range(flow.basis.degree+1):
                q = q + coeffs.water[p] * (z_right[p_prime]-z_left[p_prime]) * \
                        flow.basis.tripleNorm[p,p_prime,l]

        return swepc.FlowIncrement.array(0.0, -g*q)

    def balancedRiemannInputs(self, flow, i):
        return flow.atFace(i)

class WellBalancedEta:
    def __call__(self, g, flow, i, l):
        coeffs = flow.atElement(i)
        zPlus1 = flow.atElement(i+1).z
        zMinus1 = flow.atElement(i-1).z

        q = 0.0

        for p in range(flow.basis.degree+1):
            for p_prime in range(flow.basis.degree+1):
                q = q + coeffs.water[p] * \
                        0.5*(zPlus1[p_prime] - zMinus1[p_prime]) * \
                        flow.basis.tripleNorm[p,p_prime,l]

        return swepc.FlowIncrement.array(0.0, -g*q)

    def balancedRiemannInputs(self, flow, i):
        print("Need to make sure that q is modified to account for zStar topography")
        abort
        left, right = flow.atFace(i)

        left.z = flow.zFace[i]
        right.z = flow.zFace[i]

        return left, right

class WellBalancedH:
    def __call__(self, g, flow, i, l):
        coeffs = flow.atElement(i)
        zPlus1 = flow.atElement(i+1).z
        zMinus1 = flow.atElement(i-1).z

        q = 0.0

        for p in range(flow.basis.degree+1):
            for p_prime in range(flow.basis.degree+1):
                q = q + ((0.5*coeffs.water[p] + 0.25*coeffs.z[p]) * \
                        (zPlus1[p_prime] - zMinus1[p_prime]) - \
                        0.125*(zPlus1[p]*zPlus1[p_prime] - 
                                zMinus1[p]*zMinus1[p_prime])) * \
                        flow.basis.tripleNorm[p,p_prime,l]

        return swepc.FlowIncrement.array(0.0, -g*q)

    def balancedRiemannInputs(self, flow, i):
        left, right = flow.atFace(i)

        left = BalancedFlowCoeffsH(left, flow.zFace[i])
        right = BalancedFlowCoeffsH(right, flow.zFace[i])

        return left, right

class BalancedFlowCoeffsH:
    def __init__(self, unbalancedFlowCoeffs, zStar):
        self.water = unbalancedFlowCoeffs.water
        self.q = unbalancedFlowCoeffs.q
        self.z = unbalancedFlowCoeffs.z
        self.basis = unbalancedFlowCoeffs.basis
        self.flowValueClass = unbalancedFlowCoeffs.flowValueClass
        self.zStar = zStar

    def deterministic(self):
        return self(xi=0)

    def __call__(self, xi):
        balanced_h = self.water + self.z - self.zStar
        unbalanced_u = self.basis(xi, self.q) / self.basis(xi, self.water)
        balanced_q = unbalanced_u * self.basis(xi, balanced_h)

        return self.flowValueClass(
                self.basis(xi, balanced_h),
                balanced_q,
                self.basis(xi, self.z))
