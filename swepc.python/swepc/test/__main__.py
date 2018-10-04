import argparse
import numpy as np
import swepc
import swepc.test
import os
import sys

np.seterr(invalid='raise', divide='raise')
g = 9.80665

def main():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        description="""Uncertainty quantification for
    1D shallow water flows over uncertain topography.""")

    parser.add_argument("testCase", choices=["lakeAtRest", "criticalSteadyState"])
    parser.add_argument("solver", choices=["wellBalancedH",
        "wellBalancedEta", "centredDifferenceEta"])
    parser.add_argument("--monte-carlo", action="store_true")
    parser.add_argument("--mc-iterations", type=int, default=100)
    parser.add_argument("--mc-sample-index", type=int, default=51)
    parser.add_argument("-o", "--output-dir", required=True)
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
    elif args.testCase == "criticalSteadyState":
        testCaseClass = swepc.test.CriticalSteadyState

    mesh = swepc.Mesh(testCaseClass.domain, args.elements)

    if args.solver == "wellBalancedEta":
        solver = swepc.WellBalancedEtaSolver(g)
    if args.solver == "wellBalancedH":
        solver = swepc.WellBalancedHSolver(g)
    elif args.solver == "centredDifferenceEta":
        solver = swepc.CentredDifferenceEtaSolver(g)

    testCase = testCaseClass(mesh, solver)

    if args.end_time:
        testCase.endTime = args.end_time

    if args.monte_carlo:
        monteCarlo(args, testCase, solver, mesh)
    else:
        stochasticGalerkin(args, testCase, solver, mesh)

def stochasticGalerkin(args, testCase, solver, mesh):
    basis = swepc.GaussianHermiteBasis(args.degree)
    riemannSolver = swepc.Roe(solver.deterministicFlux, g)
    riemannEnsemble = swepc.RiemannEnsemble(
            basis, riemannSolver, quadraturePoints=args.degree+1)
    flux = swepc.StochasticFlux(basis, riemannEnsemble, solver.sourceTerm)
    flow = swepc.Flow(basis, testCase.ic, testCase.bc, solver.flowValueClass)
    sim = swepc.Simulation(g, flux, solver.sourceTerm)

    t = 0.0
    dt = args.dt

    while t < testCase.endTime:
        t = t + dt
        if t > testCase.endTime:
            dt = testCase.endTime - (t - dt)
            t = testCase.endTime

        sim.timestep(flow, mesh.dx, dt)

    stats = swepc.FlowStatistics(flow)

    with open(os.path.join(args.output_dir, "coefficients.dat"), 'w') as out:
        write(mesh, flow, solver, basis.degree, file=out)

    with open(os.path.join(args.output_dir, "statistics.dat"), 'w') as out:
        write(mesh, stats, solver, stats.moments-1, file=out)

def monteCarlo(args, testCase, solver, mesh):
    np.random.seed(0)
    sim = swepc.MonteCarlo(g, solver)

    with open(os.path.join(args.output_dir, "convergence.dat"), 'w') as out:
        print("# Sampling at x =", mesh.C[args.mc_sample_index], file=out)

        flows, stats = sim.simulate(testCase.ic, testCase.bc,
                testCase.randomTopographyGenerator(),
                mesh.dx, args.dt, testCase.endTime,
                iterations=args.mc_iterations,
                sampleIndex=args.mc_sample_index,
                file=out)

    with open(os.path.join(args.output_dir, "statistics.dat"), 'w') as out:
        write(mesh, stats, solver, degree=3, file=out)

    for i in range(mesh.elements):
        with open(os.path.join(args.output_dir, "sample"+str(i)+".dat"),
                'w') as out:
            print("# Sampling at x =", mesh.C[i], file=out)

            print("# z " + solver.water + " q", file=out)
            for flow in flows:
                print(flow.z[i,0], end=' ', file=out)
                print(flow.water[i,0], end=' ', file=out)
                print(flow.q[i,0], end=' ', file=out)
                print(file=out)

def write(mesh, flow, solver, degree, file=sys.stdout):
    print("# x", end=' ', file=file)
    for p in range(degree+1):
        print("z"+str(p), end=' ', file=file)
        print(solver.water+str(p), end=' ', file=file)
        print("q"+str(p), end=' ', file=file)
    print(file=file)

    for i in range(flow.elements):
        print(mesh.C[i], end=' ', file=file)
        for p in range(degree+1):
            print(flow.z[i,p], end=' ', file=file)
            print(flow.water[i,p], end=' ', file=file)
            print(flow.q[i,p], end=' ', file=file)
        print(file=file)

if __name__ == '__main__':
    main()
