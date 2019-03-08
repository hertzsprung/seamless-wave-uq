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

class TsengTopography:
    def __init__(self, offset = 0.0):
        self.xs = [0.0, 50.0, 100.0, 150.0, 200.0, 250.0, 300.0, 350.0, 400.0,
                425.0, 450.0, 470.0, 475.0, 500.0, 505.0, 530.0, 550.0, 565.0,
                575.0, 600.0, 650.0, 700.0, 750.0, 800.0, 820.0, 900.0, 950.0,
                1500.0]
        self.zs = np.array([0.0, 0.0, 2.5, 5.0, 5.0, 3.0, 5.0, 5.0, 7.5, 8.0,
                9.0, 9.0, 9.1, 9.0, 9.0, 6.0, 5.5, 5.5, 5.0, 4.0, 3.0, 3.0,
                2.3, 2.0, 1.2, 0.4, 0.0, 0.0])
        self.zs = self.zs + offset

    def z0(self, x):
        target_x = x
        i1, x1 = [(i, x) for i, x in enumerate(self.xs) if x < target_x][-1]
        i2, x2 = [(i, x) for i, x in enumerate(self.xs) if x >= target_x][0]
        z1, z2 = self.zs[i1], self.zs[i2]
        m = (z2 - z1)/(x2 - x1)
        c = z1 - m*x1
        return m*target_x + c

    def z1(self, x):
        return 0.0

class RandomTsengTopography:
    def __init__(self, mesh, stddev):
        self.C = mesh.C
        self.stddev = stddev 

    def sample(self):
        offset = np.random.normal(0.0, self.stddev)
        deterministic = TsengTopography(offset)
        return [deterministic.z0(x) for x in self.C], offset
