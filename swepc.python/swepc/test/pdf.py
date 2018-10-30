import argparse
import numpy as np
import sys
import swepc

def main():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        description="""Calculate probability density function from flow coefficients for a
single element.
Input is space delimited in the format <x> <z0> <water0> <q0> <z1> <water1> <q1> ...""")

    parser.add_argument("variable", choices=['z', 'water', 'derived-eta', 'q'])
    parser.add_argument("--min", type=float, required=True)
    parser.add_argument("--max", type=float, required=True)
    parser.add_argument("--samples", type=int, default=500)

    args = parser.parse_args()

    if args.variable == 'z':
        offset = 0
    elif args.variable == 'water':
        offset = 1
    else:
        offset = 2

    tokens = sys.stdin.readlines()[0].rstrip().split(' ')

    basis = swepc.GaussianHermiteBasis(degree=(len(tokens)-1)//3 - 1)
    if args.variable == 'derived-eta':
        coeffs = derivedEtaCoefficients(tokens, basis)
    else:
        coeffs = coefficients(tokens, basis, offset)

    print("# sample at x =", tokens[0])
    print("# coefficients", coeffs)

    u = np.linspace(args.min, args.max, args.samples)
    pdf = swepc.PDF(basis)(u, coeffs)

    for u, P in zip(u, pdf):
        print(u, P)

def coefficients(tokens, basis, offset):
    indices = [1+offset+3*p for p in range(basis.degree+1)]
    return [float(tokens[i]) for i in indices]

def derivedEtaCoefficients(tokens, basis):
    z_indices = [1+3*p for p in range(basis.degree+1)]
    h_indices = [2+3*p for p in range(basis.degree+1)]

    return [float(tokens[zi])+float(tokens[hi]) for zi, hi in zip(z_indices, h_indices)]
