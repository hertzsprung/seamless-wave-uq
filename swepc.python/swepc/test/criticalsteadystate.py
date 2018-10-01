import swepc

class CriticalSteadyState:
    domain = [-50.0, 50.0]

    def __init__(self, mesh, solver):
        self.endTime = 500.0
        self.ic = swepc.InitialConditions(mesh.elements, degree=1)

        bump = swepc.test.Bump(a_mean=0.6, a_stddev=0.3, halfWidth=10.0)
        self.ic.z[:,0] = [bump.z0(x) for x in mesh.C]
        self.ic.z[:,1] = [bump.z1(x) for x in mesh.C]

        self.ic.water[:,0] = [solver.elevationToWater(1.5, z)
                for z in self.ic.z[:,0]]

        self.bc = swepc.BoundaryConditions()
        self.bc.upstream_q = [1.65, 0.0]
        self.bc.downstream_water = [1.5, 0.0]
