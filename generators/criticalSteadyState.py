from ninjaopenfoam import Gnuplot, PDFLaTeXFigure, SWEPC, SWEPDF, SWEMonteCarlo
import os

class CriticalSteadyState:
    def __init__(self, degree=3, iterations=50, sampleIndex=51, elements=100,
            endTime=500.0, dt=0.15):
        self.wellBalancedH = SWEPC(
            'criticalSteadyState-wellBalancedH',
            output='uq/criticalSteadyState-wellBalancedH',
            testCase='criticalSteadyState',
            solver='wellBalancedH',
            degree=degree,
            elements=elements,
            endTime=endTime,
            dt=dt)

        self.pdf12 = SWEPDF(
            'criticalSteadyState-wellBalancedH-pdf12',
            output='uq/criticalSteadyState-wellBalancedH/pdf12',
            coefficientsFile='uq/criticalSteadyState-wellBalancedH/coefficients.dat',
            variable='derived-eta',
            sampleIndex=12,
            min=0.0,
            max=2.5,
            samples=500)

        self.pdf51 = SWEPDF(
            'criticalSteadyState-wellBalancedH-pdf51',
            output='uq/criticalSteadyState-wellBalancedH/pdf51',
            coefficientsFile='uq/criticalSteadyState-wellBalancedH/coefficients.dat',
            variable='derived-eta',
            sampleIndex=51,
            min=0.0,
            max=2.5,
            samples=500)

        self.monteCarlo = SWEMonteCarlo(
            'criticalSteadyState-monteCarlo',
            output='uq/criticalSteadyState-monteCarlo',
            testCase='criticalSteadyState',
            solver='wellBalancedH',
            iterations=iterations,
            sampleIndex=sampleIndex,
            elements=elements,
            endTime=endTime,
            dt=dt)

        self.deterministicMinusSigma = SWEPC(
            'criticalSteadyState-deterministic-sigma',
            output='uq/criticalSteadyState-deterministic-sigma',
            testCase='criticalSteadyState',
            solver='wellBalancedH',
            degree=0,
            elements=elements,
            endTime=endTime,
            dt=dt,
            topographyMean=0.3)

        self.deterministicMean = SWEPC(
            'criticalSteadyState-deterministic-mean',
            output='uq/criticalSteadyState-deterministic-mean',
            testCase='criticalSteadyState',
            solver='wellBalancedH',
            degree=0,
            elements=elements,
            endTime=endTime,
            dt=dt,
            topographyMean=0.6)

        self.deterministicPlusSigma = SWEPC(
            'criticalSteadyState-deterministic+sigma',
            output='uq/criticalSteadyState-deterministic+sigma',
            testCase='criticalSteadyState',
            solver='wellBalancedH',
            degree=0,
            elements=elements,
            endTime=endTime,
            dt=dt,
            topographyMean=0.9)

        self.deterministicPlus2Sigma = SWEPC(
            'criticalSteadyState-deterministic+2sigma',
            output='uq/criticalSteadyState-deterministic+2sigma',
            testCase='criticalSteadyState',
            solver='wellBalancedH',
            degree=0,
            elements=elements,
            endTime=endTime,
            dt=dt,
            topographyMean=1.2)

        self.examplesPlot = Gnuplot(
            'criticalSteadyState-examples',
            output=os.path.join('uq/criticalSteadyState-examples'),
            plot=os.path.join('src/uq/criticalSteadyState-examples.plt'),
            data=self.deterministicMinusSigma.outputs() + \
                    self.deterministicMean.outputs() + \
                    self.deterministicPlusSigma.outputs() + \
                    self.deterministicPlus2Sigma.outputs())

        self.examplesFigure = PDFLaTeXFigure(
            'fig-criticalSteadyState-examples',
            output=os.path.join('uq/fig-criticalSteadyState-examples'),
            figure=os.path.join('src/uq/fig-criticalSteadyState-examples'),
            components=self.examplesPlot.outputs())

        self.flowPlot = Gnuplot(
            'criticalSteadyState-flow',
            output=os.path.join('uq/criticalSteadyState-flow'),
            plot=os.path.join('src/uq/criticalSteadyState-flow.plt'),
            data=self.wellBalancedH.outputs() +
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
        return self.examplesFigure.outputs() + \
                self.flowFigure.outputs() + \
                self.pdfFigure.outputs()

    def addTo(self, build):
        build.add(self.wellBalancedH)
        build.add(self.pdf12)
        build.add(self.pdf51)
        build.add(self.monteCarlo)
        build.add(self.deterministicMinusSigma)
        build.add(self.deterministicMean)
        build.add(self.deterministicPlusSigma)
        build.add(self.deterministicPlus2Sigma)
        build.add(self.examplesPlot)
        build.add(self.examplesFigure)
        build.add(self.flowPlot)
        build.add(self.flowFigure)
        build.add(self.pdfPlot)
        build.add(self.pdfFigure)
