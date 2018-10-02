from ninjaopenfoam import Gnuplot, PDFLaTeXFigure, SWEPC
import os

class CriticalSteadyState:
    def __init__(self, degree=3, elements=100, endTime=500.0, dt=0.15):
        self.centredDifferenceEta = SWEPC(
            'criticalSteadyState-centredDifferenceEta',
            output='uq/criticalSteadyState-centredDifferenceEta.dat',
            testCase='criticalSteadyState',
            solver='centredDifferenceEta',
            degree=degree,
            elements=elements,
            endTime=endTime,
            dt=dt)

        self.wellBalancedEta = SWEPC(
            'criticalSteadyState-wellBalancedEta',
            output='uq/criticalSteadyState-wellBalancedEta.dat',
            testCase='criticalSteadyState',
            solver='wellBalancedEta',
            degree=degree,
            elements=elements,
            endTime=endTime,
            dt=dt)

        self.plot = Gnuplot(
            'criticalSteadyState',
            output=os.path.join('uq/criticalSteadyState'),
            plot=os.path.join('src/uq/criticalSteadyState.plt'),
            data=self.wellBalancedEta.outputs() + 
                 self.centredDifferenceEta.outputs())

        self.figure = PDFLaTeXFigure(
            'fig-criticalSteadyState',
            output=os.path.join('uq/fig-criticalSteadyState'),
            figure=os.path.join('src/uq/fig-criticalSteadyState'),
            components=self.plot.outputs())

    def outputs(self):
        return self.figure.outputs()

    def addTo(self, build):
        build.add(self.centredDifferenceEta)
        build.add(self.wellBalancedEta)
        build.add(self.plot)
        build.add(self.figure)
