class Simulation:
    def __init__(self, flux):
        self.flux = flux

    def timestep(self, flow, dx, dt):
        f = self.flux.evaluate(flow)

        for i in range(flow.elements):
            coeffsLeftPlus, coeffsLeftMinus = flow.atFace(i)
            coeffsRightPlus, coeffsRightMinus = flow.atFace(i+1)

            for l in range(flow.basis.degree+1):
                flow.update(i, l,
                        -dt/(dx*flow.basis.ensembleSquareOf(degree=l))
                        * (f[i+1,l] - f[i,l]))

