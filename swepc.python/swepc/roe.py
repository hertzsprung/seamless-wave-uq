import numpy as np

import swepc

class Roe:
    def __init__(self, g):
        self.g = g

    def flux(self, left, right):
        return 0.5*(left.flux(self.g) + right.flux(self.g) - \
                self.__correction(left, right))

    def __correction(self, l, r):
        mid = MidValue(l, r, self.g)

        a = np.array([mid.u + mid.c, mid.u - mid.c])
        e = [[1.0, a[0]], [1.0, a[1]]]
        alpha = [ 
                (mid.delta_q + (-mid.u + mid.c) * mid.delta_h)/(2*mid.c),
                (mid.delta_q + (-mid.u - mid.c) * mid.delta_h)/(-2*mid.c)
        ]

        return swepc.FlowValue.fromarray(np.dot(alpha * self.__Psi(a), e))

    def __Psi(self, a):
        # TODO: entropy correction
        return np.array(a)

class MidValue:
    def __init__(self, l, r, g):
        self.h = 0.5*(l.h + r.h)
        self.c = np.sqrt(g*self.h)
        self.u = (l.u()*l.c(g) + r.u()*r.c(g))/(l.c(g) + r.c(g))
        self.delta_h = r.h - l.h
        self.delta_q = r.q - l.q
