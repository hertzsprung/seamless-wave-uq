import swepc
import numpy as np
import scipy.optimize
import os

class TsengSteadyState:
    eta = 15.0
    domain = [0.0, 1500.0]

    def __init__(self, mesh, solver, args):
        self.mesh = mesh
        self.endTime = 10000.0
        self.ic = swepc.InitialConditions(mesh.elements, degree=1)

        topography = swepc.test.TsengTopography()

        self.ic.z[:,0] = [topography.z0(x) for x in mesh.C]
        self.ic.z[:,1] = [0.5 for x in mesh.C]

        self.ic.water[:,0] = [solver.elevationToWater(TsengSteadyState.eta, z)
                for z in self.ic.z[:,0]]
        self.ic.water[:,1] = [solver.elevationToWater(0.0, z)
                for z in self.ic.z[:,1]]

        self.bc = swepc.BoundaryConditions()
        self.bc.upstream_q = [0.75, 0.0]
        self.bc.downstream_water = [TsengSteadyState.eta, 0.0]

        z_exact = self.ic.z[:,0]
        z_exact = np.append(z_exact, z_exact[-1])
        h_exact = np.zeros(mesh.elements+1)
        h_exact[-1] = self.bc.downstream_water[0]

        for i, z, z_upstream in \
                reversed(list(zip(range(len(z_exact)), z_exact, z_exact[1:]))):
            h_upstream = h_exact[i+1]
            h_exact[i] = self.__h_exact(self.bc.upstream_q[0], h_upstream,
                    z_upstream, z, g = 9.80665)

        with open(os.path.join(args.output_dir, 'tseng_exact.dat'), 'w') as file:
            print('# x z h', file=file)
            for x, z, h in zip(mesh.C, z_exact, h_exact):
                print(x, z, h, file=file)

    def __h_exact(self, q_in, h_upstream, z_upstream, z, g):
        H = h_upstream + z_upstream + q_in**2/(2*g*h_upstream**2)
        return scipy.optimize.fsolve(
                lambda h: h**3 + (z-H)*h**2 + q_in**2/(2*g), h_upstream)

    def randomTopographyGenerator(self, args):
        return swepc.test.RandomTsengTopography(self.mesh, stddev=0.5)
