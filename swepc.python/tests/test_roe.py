import pytest

import swepc

def test_roe():
    roe = swepc.Roe(g=9.80665)
    
    left = swepc.FlowValue(h=4.0, q=0.0)
    right = swepc.FlowValue(h=5.0, q=0.0)

    flux = roe.flux(left, right)
    assert flux.h == pytest.approx(0.0)
    assert flux.q == pytest.approx(78.4532)
