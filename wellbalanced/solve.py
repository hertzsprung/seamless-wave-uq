#!/usr/bin/env python3
import numpy as np
import swepc
import matplotlib.pyplot as plt

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

def topoGradTerm(i):
    return -g*(h[i]+z[i]-zAverage[i])*(zFace[i+1] - zFace[i])

g = 9.80665
domain = [0, 50]
N = 256
dx = (domain[1] - domain[0])/N
x = np.linspace(dx/2, domain[1]-dx/2, N)
endTime = 100.0
dt = 0.02

h = np.zeros(N)
q = np.zeros(N)
z = np.zeros(N)

zFace = [topography(x) for x in np.linspace(0, domain[1], N+1)]
z[:] = [0.5*(l+r) for l, r in zip(zFace, zFace[1:])]

zFace = np.zeros(N+1)
zFace[0] = z[0]
zFace[-1] = z[-1]
zFace[1:-1] = [max(l,r) for l, r in zip(z, z[1:])]
zAverage = np.zeros(N)
zAverage[:] = [0.5*(l+r) for l, r in zip(zFace, zFace[1:])]

h = 2.0 - z

riemann = swepc.Roe(g)

f, axes = plt.subplots(2, sharex=True)

c = 0
t = 0.0
while t < endTime:
    flux = np.zeros(N+1, dtype=swepc.FlowValue)

    for i in range(N+1):
        if i == 0:
            left = swepc.FlowValue(h[0], q[0])
            right = left
        elif i == N:
            left = swepc.FlowValue(h[-1], q[-1])
            right = left
        else:
            left = swepc.FlowValue(h[i-1], q[i-1])
            left_h = h[i-1]+z[i-1]-zFace[i]
            left = swepc.FlowValue(left_h, left.u()*left_h)

            right = swepc.FlowValue(h[i], q[i])
            right_h = h[i]+z[i]-zFace[i]
            right = swepc.FlowValue(right_h, right.u()*right_h)

        flux[i] = riemann.flux(left, right)

    for i in range(N):
        h[i] -= dt/dx * (flux[i+1] - flux[i]).h
        q[i] -= dt/dx * ((flux[i+1] - flux[i]).q - topoGradTerm(i))

    t += dt
    c += 1
    
    if c % 8 == 0:
        axes[0].cla()
        axes[0].annotate("$t$ = {0:.3f}".format(t), (0, 0), xycoords='axes fraction')
        axes[0].plot(x, z)
        axes[0].plot(x, z+h)
        axes[1].cla()
        axes[1].plot(x, q)
        plt.draw()
        plt.pause(0.01)
