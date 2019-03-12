from ninjaopenfoam import Gnuplot, PDFLaTeXFigure, SWEPC
import os

class TsengSteadyState:
    def __init__(self):
        self.sg3 = SWEPC(
            'tsengSteadyState-wellBalancedH-3',
            output='uq/tsengSteadyState-wellBalancedH-3',
            testCase='tsengSteadyState',
            solver='wellBalancedH',
            degree=3,
            elements=200,
            endTime=100000.0,
            dt=0.5)
        
        self.flowPlot = Gnuplot(
            'tsengSteadyState-flow',
            output=os.path.join('uq/tsengSteadyState-flow'),
            plot=os.path.join('src/uq/tsengSteadyState-flow.plt'),
            data=self.sg3.outputs())

        self.flowFigure = PDFLaTeXFigure(
            'fig-tsengSteadyState-flow',
            output=os.path.join('uq/fig-tsengSteadyState-flow'),
            figure=os.path.join('src/uq/fig-tsengSteadyState-flow'),
            components=self.flowPlot.outputs())

    def outputs(self):
        return self.flowFigure.outputs()

    def addTo(self, build):
        build.add(self.sg3)
        build.add(self.flowPlot)
        build.add(self.flowFigure)
