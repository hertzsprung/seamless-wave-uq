import swepc

class LakeAtRest:
    domain = [-50.0, 50.0]

    def __init__(self, mesh, solver, args):
        self.endTime = 100.0
        self.ic = swepc.InitialConditions(mesh.elements, degree=1)

        bump = swepc.test.TwoBumps(args.topography_mean,
                args.topography_stddev, halfWidth=10.0)
        self.ic.z[:,0] = [bump.z0(x) for x in mesh.C]
        self.ic.z[:,1] = [bump.z1(x) for x in mesh.C]

        self.ic.water[:,0] = [solver.elevationToWater(1.5, z)
                for z in self.ic.z[:,0]]
        self.ic.water[:,1] = [solver.elevationToWater(0.0, z)
                for z in self.ic.z[:,1]]

        self.bc = swepc.BoundaryConditions()
