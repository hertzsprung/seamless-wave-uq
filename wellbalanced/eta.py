#!/usr/bin/env python3
import numpy as np
import swepc
import matplotlib.pyplot as plt

# it is nasty to have z in here because it makes no sense for add, sub
# mul operations to be defined.
class EtaFlowValue:
    def __init__(self, eta, q, z=0.0):
        self.eta = eta
        self.q = q
        self.z = z
        self.h = self.eta - self.z

    def flux(self, g):
        return swepc.FlowValue(self.q, self.q**2/self.h + 0.5*g*
                (self.eta**2 - 2.0*self.eta*self.z))

    @classmethod
    def fromarray(cls, array):
        return cls(array[0], array[1])

    def u(self):
        return self.q / self.h

    def c(self, g):
        return np.sqrt(g*self.h)

    def __add__(self, other):
        return FlowValue(self.eta+other.eta, self.q+other.q)

    def __sub__(self, other):
        return FlowValue(self.eta-other.eta, self.q-other.q)

    def __mul__(self, scalar):
        return FlowValue(scalar*self.eta, scalar*self.q)
    
    def __rmul__(self, scalar):
        return FlowValue(scalar*self.eta, scalar*self.q)

    def __str__(self):
        return "FlowValue<h={h},q={q}>".format(h=self.h, q=self.q)

    __repr__ = __str__

def topography(x):
    z = 0.0

    if 8 < x and x <= 12:
        z = 2.0 - 0.5*pow(x-10, 2)
    elif 22 < x <= 25:
        z = 0.5*x - 11.0
    elif 25 < x <= 28:
        z = -0.5*x + 14.0
    elif 39 < x <= 46:
        z = 3.0

    return z*0.5

def topoGradTerm(faceFlow, i):
    return -g*eta[i]*zGrad[i]

g = 9.80665
domain = [0, 50]
N = 256
dx = (domain[1] - domain[0])/N
x = np.linspace(dx/2, domain[1]-dx/2, N)
endTime = 100.0
dt = 0.02

eta = np.zeros(N)
q = np.zeros(N)
z = np.zeros(N)

zFace = [topography(x) for x in np.linspace(0, domain[1], N+1)]
z[:] = [0.5*(l+r) for l, r in zip(zFace, zFace[1:])]

zFace = np.zeros(N+1)
zFace[0] = z[0]
zFace[-1] = z[-1]
zFace[1:-1] = [0.5*(l+r) for l, r in zip(z, z[1:])]

zGrad = np.zeros(N)
zGrad[:] = [r-l for l, r in zip(zFace, zFace[1:])]

eta[:] = 2.0

riemann = swepc.Roe(g)

f, axes = plt.subplots(2, sharex=True)

c = 0
t = 0.0
while t < endTime:
    faceFlow = np.empty(2*(N+1), dtype=EtaFlowValue)
    flux = np.zeros(N+1, dtype=swepc.FlowValue)

    for i in range(N+1):
        if i == 0:
            faceFlow[0] = EtaFlowValue(eta[0], q[0], zFace[0])
            faceFlow[1] = EtaFlowValue(eta[0], q[0], zFace[0])
        elif i == N:
            faceFlow[-2] = EtaFlowValue(eta[-1], q[-1], zFace[-1])
            faceFlow[-1] = EtaFlowValue(eta[-1], q[-1], zFace[-1])
        else:
            faceFlow[2*i] = EtaFlowValue(eta[i-1], q[i-1], zFace[i])
            faceFlow[2*i+1] = EtaFlowValue(eta[i], q[i], zFace[i])

    for i in range(N+1):
        flux[i] = riemann.flux(faceFlow[2*i], faceFlow[2*i+1])

    for i in range(N):
        eta[i] -= dt/dx * (flux[i+1] - flux[i]).h
        q[i] -= dt/dx * ((flux[i+1] - flux[i]).q - topoGradTerm(faceFlow, i))

    t += dt
    c += 1
    
    if c % 8 == 0:
        axes[0].cla()
        axes[0].annotate("$t$ = {0:.3f}".format(t), (0, 0), xycoords='axes fraction')
        axes[0].plot(x, z)
        axes[0].plot(x, eta)
        axes[1].cla()
        axes[1].plot(x, q)
        plt.draw()
        plt.pause(0.01)
