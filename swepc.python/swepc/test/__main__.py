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

    parser.add_argument("testCase", choices=["lakeAtRest", "criticalSteadyState", "tsengSteadyState"])
    parser.add_argument("solver", choices=["wellBalancedH",
        "wellBalancedEta", "centredDifferenceH"])
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
    parser.add_argument("--topography-mean", type=float, default=0.6)
    parser.add_argument("--topography-stddev", type=float, default=0.3)
    parser.add_argument("--water-convergence", action="store_true")

    args = parser.parse_args()

    if args.testCase == "lakeAtRest":
        testCaseClass = swepc.test.LakeAtRest
    elif args.testCase == "criticalSteadyState":
        testCaseClass = swepc.test.CriticalSteadyState
    elif args.testCase == "tsengSteadyState":
        testCaseClass = swepc.test.TsengSteadyState

    mesh = swepc.Mesh(testCaseClass.domain, args.elements)

    if args.solver == "wellBalancedEta":
        solver = swepc.WellBalancedEtaSolver(g)
    if args.solver == "wellBalancedH":
        solver = swepc.WellBalancedHSolver(g)
    elif args.solver == "centredDifferenceH":
        solver = swepc.CentredDifferenceHSolver(g)

    testCase = testCaseClass(mesh, solver, args)

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

    convergence = swepc.Convergence(flow)

    with open(os.path.join(args.output_dir, "convergence.dat"), 'w') as out:
        print('# t l2(h)', file=out)

        c = 0
        while t < testCase.endTime:
            t = t + dt
            if t > testCase.endTime:
                dt = testCase.endTime - (t - dt)
                t = testCase.endTime

            sim.timestep(flow, mesh.dx, dt)

            if c % 20 == 0:
                cfl = 0.0
                for i in range(flow.elements):
                    U = flow.atElement(i).deterministic()
                    cfl = max(cfl, dt/mesh.dx*np.abs(U.u())*np.sqrt(sim.g*U.h))
                print(t, cfl)
            c = c + 1

            if args.water_convergence:
                print(t, convergence(flow), file=out)

    stats = swepc.FlowStatistics(flow)

    with open(os.path.join(args.output_dir, "coefficients.dat"), 'w') as out:
        write(mesh, flow, solver, basis.degree, file=out)

    with open(os.path.join(args.output_dir, "statistics.dat"), 'w') as out:
        write(mesh, stats, solver, stats.moments-1, file=out)

    with open(os.path.join(args.output_dir, "derived-statistics.dat"), 'w') as out:
        solver.writeDerivedStochasticGalerkinStatistics(mesh, flow, file=out)

def monteCarlo(args, testCase, solver, mesh):
    np.random.seed(0)
    sim = swepc.MonteCarlo(g, solver, testCase.eta)

    with open(os.path.join(args.output_dir, "convergence.dat"), 'w') as out:
        print("# Sampling at x =", mesh.C[args.mc_sample_index], file=out)

        flows, stats, z_peaks = sim.simulate(testCase.ic, testCase.bc,
                testCase.randomTopographyGenerator(args),
                mesh.dx, args.dt, testCase.endTime,
                iterations=args.mc_iterations,
                sampleIndex=args.mc_sample_index,
                file=out)

    with open(os.path.join(args.output_dir, "statistics.dat"), 'w') as out:
        write(mesh, stats, solver, degree=3, file=out)

    with open(os.path.join(args.output_dir, "derived-statistics.dat"), 'w') as out:
        solver.writeDerivedMonteCarloStatistics(mesh, flows, stats, file=out)

    for i in range(mesh.elements):
        with open(os.path.join(args.output_dir, "sample"+str(i)+".dat"),
                'w') as out:
            print("# Sampling at x =", mesh.C[i], file=out)

            print("# z " + solver.water + " q z_peak", file=out)
            for flow, z_peak in zip(flows, z_peaks):
                print(flow.z[i,0], end=' ', file=out)
                print(flow.water[i,0], end=' ', file=out)
                print(flow.q[i,0], end=' ', file=out)
                print(z_peak, end=' ', file=out)
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
