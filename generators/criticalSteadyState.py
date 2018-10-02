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

        self.flowPlot = Gnuplot(
            'criticalSteadyState',
            output=os.path.join('uq/criticalSteadyState-flow'),
            plot=os.path.join('src/uq/criticalSteadyState-flow.plt'),
            data=self.wellBalancedEta.outputs() +
                 self.monteCarlo.outputs())

        self.flowFigure = PDFLaTeXFigure(
            'fig-criticalSteadyStateFlow',
            output=os.path.join('uq/fig-criticalSteadyState-flow'),
            figure=os.path.join('src/uq/fig-criticalSteadyState-flow'),
            components=self.flowPlot.outputs())

    def outputs(self):
        return self.figure.outputs()

    def addTo(self, build):
        build.add(self.wellBalancedEta)
        build.add(self.monteCarlo)
        build.add(self.flowPlot)
        build.add(self.flowFigure)
