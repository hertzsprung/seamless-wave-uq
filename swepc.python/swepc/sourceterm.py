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
        preserveElevation = lambda U, z: \
                swepc.FlowCoeffs(U.water + U.z - z, U.q, U.z, U.basis,
                        swepc.FlowValueH)

        left, right = flow.atFace(i)

        left = preserveElevation(left, flow.zFace[i])
        right = preserveElevation(right, flow.zFace[i])

        return left, right
