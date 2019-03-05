import swepc

class EDFSteadyState:
    domain = [0.0, 1500.0]

    def __init__(self, mesh, solver, args):
        self.mesh = mesh
        self.endTime = 10000.0
        self.ic = swepc.InitialConditions(mesh.elements, degree=1)

        topography = swepc.test.EDF()

        self.ic.z[:,0] = [topography.z0(x) for x in mesh.C]
        self.ic.z[:,1] = [0.5 for x in mesh.C]

        self.ic.water[:,0] = [solver.elevationToWater(15.0, z)
                for z in self.ic.z[:,0]]
        self.ic.water[:,1] = [solver.elevationToWater(0.0, z)
                for z in self.ic.z[:,1]]

        self.bc = swepc.BoundaryConditions()
        self.bc.upstream_q = [0.75, 0.0]
        self.bc.downstream_water = [15.0, 0.0]
