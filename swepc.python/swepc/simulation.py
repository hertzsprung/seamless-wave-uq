import swepc

class Simulation:
    def __init__(self, g, flux, sourceTerm):
        self.g = g
        self.flux = flux
        self.sourceTerm = sourceTerm

    def timestep(self, flow, dx, dt):
        f = self.flux(flow)

        for i in range(flow.elements):
            for l in range(flow.basis.degree+1):
                flow.update(i, l,
                    -dt/(dx*flow.basis.squareNorm[l])
                    * (f[i+1,l] - f[i,l] -
                        self.sourceTerm(self.g, flow, i, l)))

        return flow

