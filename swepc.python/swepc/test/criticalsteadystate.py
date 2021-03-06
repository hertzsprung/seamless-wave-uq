import swepc

class CriticalSteadyState:
    domain = [-50.0, 50.0]
    eta = 1.5

    def __init__(self, mesh, solver, args):
        self.mesh = mesh
        self.endTime = 500.0
        self.ic = swepc.InitialConditions(mesh.elements, degree=1)

        bump = swepc.test.Bump(args.topography_mean, args.topography_stddev,
                halfWidth=10.0)
        self.ic.z[:,0] = [bump.z0(x) for x in mesh.C]
        self.ic.z[:,1] = [bump.z1(x) for x in mesh.C]

        self.ic.water[:,0] = [solver.elevationToWater(CriticalSteadyState.eta, z)
                for z in self.ic.z[:,0]]
        self.ic.water[:,1] = [solver.elevationToWater(0.0, z)
                for z in self.ic.z[:,1]]

        self.bc = swepc.BoundaryConditions()
        self.bc.upstream_q = [1.65, 0.0]
        self.bc.downstream_water = [CriticalSteadyState.eta, 0.0]

    def randomTopographyGenerator(self, args):
        return swepc.test.RandomSmoothBump(self.mesh, args.topography_mean,
                args.topography_stddev, halfWidth=10.0, a_min=0.0, a_max=1.4)
