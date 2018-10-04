from ninjaopenfoam import Gnuplot, PDFLaTeXFigure, SWEPC, SWEPDF, SWEMonteCarlo
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

        self.pdf12 = SWEPDF(
            'criticalSteadyState-wellBalancedEta-pdf12',
            output='uq/criticalSteadyState-wellBalancedEta/pdf12',
            coefficientsFile='uq/criticalSteadyState-wellBalancedEta/coefficients.dat',
            variable='water',
            sampleIndex=12,
            min=0.0,
            max=2.5,
            samples=500)

        self.pdf51 = SWEPDF(
            'criticalSteadyState-wellBalancedEta-pdf51',
            output='uq/criticalSteadyState-wellBalancedEta/pdf51',
            coefficientsFile='uq/criticalSteadyState-wellBalancedEta/coefficients.dat',
            variable='water',
            sampleIndex=51,
            min=0.0,
            max=2.5,
            samples=500)

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
            'criticalSteadyState-flow',
            output=os.path.join('uq/criticalSteadyState-flow'),
            plot=os.path.join('src/uq/criticalSteadyState-flow.plt'),
            data=self.wellBalancedEta.outputs() +
                 self.monteCarlo.outputs())

        self.flowFigure = PDFLaTeXFigure(
            'fig-criticalSteadyState-flow',
            output=os.path.join('uq/fig-criticalSteadyState-flow'),
            figure=os.path.join('src/uq/fig-criticalSteadyState-flow'),
            components=self.flowPlot.outputs())

        self.pdfPlot = Gnuplot(
            'criticalSteadyState-pdf',
            output=os.path.join('uq/criticalSteadyState-pdf'),
            plot=os.path.join('src/uq/criticalSteadyState-pdf.plt'),
            data=self.pdf12.outputs() +
                 self.pdf51.outputs() + 
                 self.monteCarlo.outputs())

        self.pdfFigure = PDFLaTeXFigure(
            'fig-criticalSteadyState-pdf',
            output=os.path.join('uq/fig-criticalSteadyState-pdf'),
            figure=os.path.join('src/uq/fig-criticalSteadyState-pdf'),
            components=self.pdfPlot.outputs())

    def outputs(self):
        return self.figure.outputs()

    def addTo(self, build):
        build.add(self.wellBalancedEta)
        build.add(self.pdf12)
        build.add(self.pdf51)
        build.add(self.monteCarlo)
        build.add(self.flowPlot)
        build.add(self.flowFigure)
        build.add(self.pdfPlot)
        build.add(self.pdfFigure)
