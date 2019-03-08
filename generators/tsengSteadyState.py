from ninjaopenfoam import Gnuplot, PDFLaTeXFigure
import os

class TsengSteadyState:
    def __init__(self):
        self.flowPlot = Gnuplot(
            'tsengSteadyState-flow',
            output=os.path.join('uq/tsengSteadyState-flow'),
            plot=os.path.join('src/uq/tsengSteadyState-flow.plt'))

        self.flowFigure = PDFLaTeXFigure(
            'fig-tsengSteadyState-flow',
            output=os.path.join('uq/fig-tsengSteadyState-flow'),
            figure=os.path.join('src/uq/fig-tsengSteadyState-flow'),
            components=self.flowPlot.outputs())

    def outputs(self):
        return self.flowFigure.outputs()

    def addTo(self, build):
        build.add(self.flowPlot)
        build.add(self.flowFigure)
