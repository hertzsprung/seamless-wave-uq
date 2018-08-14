#!/usr/bin/env python3
import swepc
import numpy as np
import matplotlib.pyplot as plt

g = 9.80665
basis = swepc.GaussianHermiteBasis(degree=1)
solver = swepc.Roe(g)
riemannEnsemble = swepc.RiemannEnsemble(basis, solver, quadraturePoints=4)

domain = [0.0, 50.0]
N = 64
dx = (domain[1] - domain[0])/N
xs = np.linspace(dx/2, domain[1]-dx/2, N)
dt = 0.05
endTime = 40.0

flow = swepc.Flow(N, basis)

flow.h[:,0] = 6.0
flow.h[N//2:,0] = 3.0
flow.h[:,1] = 1.0

t = 0.0
while t < endTime:
    print("#t {0:.3f}".format(t), "cfl", round(dt/dx*flow.maxWaveSpeed(g), 3))
    print()
    plt.figure(1)
    plt.clf()
    plt.plot(xs, flow.h[:,0], color='b')
    plt.plot(xs, flow.h[:,0] + flow.h[:,1], color='b', linestyle='dashed')
    plt.plot(xs, flow.h[:,0] - flow.h[:,1], color='b', linestyle='dashed')
    #plt.plot(xs, 10*flow.h[:,1])
    plt.ylim((0,10))
    plt.pause(0.001)

    for i in range(N):
        coeffsLeftPlus, coeffsLeftMinus = flow.atFace(i)
        coeffsRightPlus, coeffsRightMinus = flow.atFace(i+1)

        for l in range(basis.degree+1):
            fluxL = riemannEnsemble.integrate(coeffsLeftPlus, coeffsLeftMinus,
                    basis.polynomialOf(degree=l))
            fluxR = riemannEnsemble.integrate(coeffsRightPlus, coeffsRightMinus,
                    basis.polynomialOf(degree=l))

            flow.update(i, l, -dt/(dx*basis.ensembleSquareOf(degree=l)) * 
                    (fluxR - fluxL))

    t = t + dt 


