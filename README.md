# seamless-wave-uq
Stochastic Galerkin and Monte Carlo uncertainty quantification for 1D shallow water equations with uncertain topography.
This repository includes
* a Godunov-type finite volume solver for 1D shallow water equations with topography, which can operate as a stochastic Galerkin solver or a deterministic solver
* code for running Monte Carlo iterations of the deterministic solver
* preconfigured lake-at-rest and steady-state critical flow test cases

Build scripts are also provided that run test cases and generate the plots that appear in the accompanying article in the [ASCE Journal of Hydraulic Engineering](https://ascelibrary.org/journal/jhend8).
These scripts require [ninja-openfoam](https://github.com/hertzsprung/ninjaopenfoam) to be installed.

## Installation

Ubuntu users can install the toolchain

    apt install python3-numpy python3-scipy ninja-build gnuplot texlive-extra-utils
   
To install the Python 3 solvers
   
    pip3 install --user --editable swepc.python
    
## Usage
    
To run the stochastic Galerkin solver

    swepc lakeAtRest wellBalancedH -o /tmp
    
will run the lake-at-rest test with the [well-balanced surface gradient method](https://doi.org/10.1006/jcph.2000.6670).

To run a Monte Carlo simulation with 10 iterations of critical steady-state flow 

    swepc --monte-carlo --mc-iterations 10 criticalSteadyState wellBalancedH -o /tmp
