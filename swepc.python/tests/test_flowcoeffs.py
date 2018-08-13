import pytest

import swepc

def test_flowcoeffs():
    basis = swepc.GaussianHermiteBasis(degree=1)
    coeffs = swepc.FlowCoeffs([4.0, 0.5], [3.0, 0.1], basis)

    value = coeffs(xi=1.0)
    assert value.h == pytest.approx(4.5)
    assert value.q == pytest.approx(3.1)
