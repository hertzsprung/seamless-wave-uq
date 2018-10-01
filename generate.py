#!/usr/bin/env python3
from ninjaopenfoam import Build, Gnuplot, PDFLaTeXFigure, SWEPC
import os

degree=3
elements=100
endTime=10.0
dt=0.1

lakeAtRest_centredDifferenceEta = SWEPC(
        'lakeAtRest-centredDifferenceEta',
        output='uq/lakeAtRest-centredDifferenceEta.dat',
        testCase='lakeAtRest',
        solver='centredDifferenceEta',
        degree=degree,
        elements=elements,
        endTime=endTime,
        dt=dt)

lakeAtRest_wellBalancedH = SWEPC(
        'lakeAtRest-wellBalancedH',
        output='uq/lakeAtRest-wellBalancedH.dat',
        testCase='lakeAtRest',
        solver='wellBalancedH',
        degree=degree,
        elements=elements,
        endTime=endTime,
        dt=dt)

lakeAtRest_wellBalancedEta = SWEPC(
        'lakeAtRest-wellBalancedEta',
        output='uq/lakeAtRest-wellBalancedEta.dat',
        testCase='lakeAtRest',
        solver='wellBalancedEta',
        degree=degree,
        elements=elements,
        endTime=endTime,
        dt=dt)

lakeAtRest = Gnuplot(
    'lakeAtRest',
    output=os.path.join('uq/lakeatrest'),
    plot=os.path.join('src/uq/lakeatrest.plt'),
    data=lakeAtRest_wellBalancedEta.outputs() + 
         lakeAtRest_wellBalancedH.outputs() + 
         lakeAtRest_centredDifferenceEta.outputs())

lakeAtRestFigure = PDFLaTeXFigure(
    'fig-lakeAtRest',
    output=os.path.join('uq/fig-lakeatrest'),
    figure=os.path.join('src/uq/fig-lakeatrest'),
    components=lakeAtRest.outputs())

build = Build()
build.add(lakeAtRest_centredDifferenceEta)
build.add(lakeAtRest_wellBalancedEta)
build.add(lakeAtRest_wellBalancedH)
build.add(lakeAtRest)
build.add(lakeAtRestFigure)
build.write()
