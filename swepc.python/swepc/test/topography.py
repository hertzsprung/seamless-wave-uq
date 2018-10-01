import numpy as np

class Bump:
    def __init__(self, a_mean, a_stddev, halfWidth):
        self.a_mean = a_mean
        self.a_stddev = a_stddev
        self.halfWidth = halfWidth

    def z0(self, x):
        return self.a_mean*(1/np.cosh(np.pi/self.halfWidth*x))**2

    def z1(self, x):
        return np.sqrt(self.__dzda(x)**2 * self.a_stddev**2)

    def __dzda(self, x):
        return (1/np.cosh(np.pi/self.halfWidth*x))**2

class TwoBumps:
    def __init__(self, a_mean, a_stddev, halfWidth):
        self.bump = Bump(a_mean, a_stddev, halfWidth)

    def z0(self, x):
        z = 0.0

        if 30 < x and x <= 40:
            z = self.bump.a_mean

        return z + self.bump.z0(x)

    def z1(self, x):
        return self.bump.z1(x)

