import swepc

class Simulation:
    def __init__(self, g, flux):
        self.g = g
        self.flux = flux

    def timestep(self, flow, dx, dt):
        f = self.flux.evaluate(flow)

        for i in range(flow.elements):
            coeffsLeftPlus, coeffsLeftMinus = flow.atFace(i)
            coeffsRightPlus, coeffsRightMinus = flow.atFace(i+1)

            for l in range(flow.basis.degree+1):
                flow.update(i, l,
                    -dt/(dx*flow.basis.squareNorm[l])
                    * (f[i+1,l] - f[i,l] -
                        self.__topography(flow, i, l)))

        return flow

    def __topography(self, flow, i, l):
        coeffs = flow.atElement(i)
        zPlus1 = flow.atElement(i+1).z
        zMinus1 = flow.atElement(i-1).z

        q = 0.0

        for p in range(flow.basis.degree+1):
            for p_prime in range(flow.basis.degree+1):
                q = q + ((0.5*coeffs.h[p] + 0.25*coeffs.z[p]) * \
                        (zPlus1[p_prime] - zMinus1[p_prime]) - \
                        0.125*(zPlus1[p]*zPlus1[p_prime] - 
                                zMinus1[p]*zMinus1[p_prime])) * \
                        flow.basis.tripleNorm[p,p_prime,l]

        return swepc.FlowValue(0.0, -self.g*q)

