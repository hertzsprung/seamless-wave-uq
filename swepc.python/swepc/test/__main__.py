import argparse
import swepc
import swepc.test

def main():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        description="""Uncertainty quantification for
    1D shallow water flows over uncertain topography.""")

    parser.add_argument("testCase", choices=["lakeAtRest", "criticalSteadyState"])
    parser.add_argument("solver", choices=["wellBalancedH",
        "wellBalancedEta", "centredDifferenceEta"])
    parser.add_argument("-d", "--degree", type=int, default=3,
            help="Polynomial chaos degree")
    parser.add_argument("-M", "--elements", type=int, default=100,
            help="Number of mesh elements")
    parser.add_argument("--end-time", type=float,
            help="Override default test case-dependent end time")
    parser.add_argument("--dt", type=float, default=0.15)

    args = parser.parse_args()

    if args.testCase == "lakeAtRest":
        testCaseClass = swepc.test.LakeAtRest

    mesh = swepc.Mesh(testCaseClass.domain, args.elements)

    g = 9.80665

    if args.solver == "wellBalancedEta":
        solver = swepc.WellBalancedEtaSolver(g)
    if args.solver == "wellBalancedH":
        solver = swepc.WellBalancedHSolver(g)
    elif args.solver == "centredDifferenceEta":
        solver = swepc.CentredDifferenceEtaSolver(g)

    testCase = testCaseClass(mesh, solver)

    basis = swepc.GaussianHermiteBasis(args.degree)
    riemannSolver = swepc.Roe(solver.deterministicFlux, g)
    riemannEnsemble = swepc.RiemannEnsemble(
            basis, riemannSolver, quadraturePoints=args.degree+1)
    flux = swepc.StochasticFlux(basis, riemannEnsemble, solver.sourceTerm)
    flow = swepc.Flow(basis, testCase.ic, testCase.bc, solver.flowValueClass)
    sim = swepc.Simulation(g, flux, solver.sourceTerm)

    t = 0.0
    dt = args.dt
    if "end_time" in vars(args):
        testCase.endTime = args.end_time

    while t < testCase.endTime:
        t = t + dt
        if t > testCase.endTime:
            dt = testCase.endTime - (t - dt)
            t = testCase.endTime

        sim.timestep(flow, mesh.dx, dt)

    print("# x", end=' ')
    for p in range(basis.degree):
        print("z"+str(p), end=' ')
        print(solver.water+str(p), end=' ')
        print("q"+str(p), end=' ')
    print()

    for i in range(flow.elements):
        print(mesh.C[i], end=' ')
        for p in range(basis.degree):
            print(flow.z[i,p], end=' ')
            print(flow.water[i,p], end=' ')
            print(flow.q[i,p], end=' ')
        print()

if __name__ == '__main__':
    main()
