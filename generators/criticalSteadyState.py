from ninjaopenfoam import Gnuplot, PDFLaTeXFigure, SWEPC, SWEMonteCarlo
import os

class CriticalSteadyState:
    def __init__(self, degree=3, iterations=1000, sampleIndex=51, elements=100,
            endTime=500.0, dt=0.15):
        self.wellBalancedEta = SWEPC(
            'criticalSteadyState-wellBalancedEta',
            output='uq/criticalSteadyState-wellBalancedEta',
            testCase='criticalSteadyState',
            solver='wellBalancedEta',
            degree=degree,
            elements=elements,
            endTime=endTime,
            dt=dt)

        self.monteCarlo = SWEMonteCarlo(
            'criticalSteadyState-monteCarlo',
            output='uq/criticalSteadyState-monteCarlo',
            testCase='criticalSteadyState',
            solver='wellBalancedEta',
            iterations=iterations,
            sampleIndex=sampleIndex,
            elements=elements,
            endTime=endTime,
            dt=dt)

        self.plot = Gnuplot(
            'criticalSteadyState',
            output=os.path.join('uq/criticalSteadyState'),
            plot=os.path.join('src/uq/criticalSteadyState.plt'),
            data=self.wellBalancedEta.outputs() +
                 self.monteCarlo.outputs())

        self.figure = PDFLaTeXFigure(
            'fig-criticalSteadyState',
            output=os.path.join('uq/fig-criticalSteadyState'),
            figure=os.path.join('src/uq/fig-criticalSteadyState'),
            components=self.plot.outputs())

    def outputs(self):
        return self.figure.outputs()

    def addTo(self, build):
        build.add(self.wellBalancedEta)
        build.add(self.monteCarlo)
        build.add(self.plot)
        build.add(self.figure)
