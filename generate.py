#!/usr/bin/env python3
from ninjaopenfoam import Build

import generators
import os

build = Build([
    'generators/lakeAtRest.py',
    'generators/criticalSteadyState.py',
    'generators/tsengSteadyState.py'
])

lakeAtRest = generators.LakeAtRest()
criticalSteadyState = generators.CriticalSteadyState(iterations=2000)
tsengSteadyState = generators.TsengSteadyState()

lakeAtRest.addTo(build)
criticalSteadyState.addTo(build)
tsengSteadyState.addTo(build)

build.write()
