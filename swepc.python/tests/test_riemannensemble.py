import pytest

import swepc

def test_riemannensemble():
    basis = swepc.GaussianHermiteBasis(degree=1)
    solver = swepc.Roe(g=9.80665)
    riemannEnsemble = swepc.RiemannEnsemble(basis, solver, quadraturePoints=2)

    left = swepc.FlowCoeffs([4.0, 1.0], [0.0, 0.0], basis)
    right = swepc.FlowCoeffs([4.0, 0.0], [0.0, 0.0], basis)

    value = riemannEnsemble.integrate(left, right, basis.polynomialOf(degree=1))
    print(value)
