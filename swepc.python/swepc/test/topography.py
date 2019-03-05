import numpy as np
import sys

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

class RandomSmoothBump:
    def __init__(self, mesh, a_mean, a_stddev, halfWidth, a_min, a_max):
        self.C = mesh.C
        self.a_mean = a_mean
        self.a_stddev = a_stddev
        self.halfWidth = halfWidth
        self.a_min = a_min
        self.a_max = a_max

    def sample(self):
        a = np.random.normal(self.a_mean, self.a_stddev)
        while a < self.a_min or a > self.a_max:
            print("# rejecting a =", a, file=sys.stderr)
            a = np.random.normal(self.a_mean, self.a_stddev)
        bump = Bump(a, 0.0, self.halfWidth)
        return [bump.z0(x) for x in self.C], a

class EDF:
    def z0(self, x):
        if x <= 50.0:
            return 0.0
        elif x <= 100.0:
            return 2.5
        elif x <= 200.0:
            return 5.0
        elif x <= 250.0:
            return 3.0
        elif x <= 350.0:
            return 5.0
        elif x <= 400.0:
            return 7.5
        elif x <= 425.0:
            return 8.0
        elif x <= 470.0:
            return 9.0
        elif x <= 475.0:
            return 9.1
        elif x <= 505.0:
            return 9.0
        elif x <= 530.0:
            return 6.0
        elif x <= 565.0:
            return 5.5
        elif x <= 575.0:
            return 5.0
        elif x <= 600.0:
            return 4.0
        elif x <= 700.0:
            return 3.0
        elif x <= 750.0:
            return 2.3
        elif x <= 800.0:
            return 2.0
        elif x <= 820.0:
            return 1.2
        elif x <= 900.0:
            return 0.4
        else:
            return 0.0

    def z1(self, x):
        return 0.0
