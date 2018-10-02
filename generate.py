#!/usr/bin/env python3
from ninjaopenfoam import Build

import generators
import os

build = Build([
    'generators/lakeAtRest.py',
    'generators/criticalSteadyState.py'
])

criticalSteadyState = generators.CriticalSteadyState(iterations=200)
lakeAtRest = generators.LakeAtRest()

criticalSteadyState.addTo(build)
lakeAtRest.addTo(build)

build.write()
