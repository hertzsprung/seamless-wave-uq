from ninjaopenfoam import Gnuplot, PDFLaTeXFigure, SWEPC
import os

class LakeAtRest:
    def __init__(self, degree=3, elements=100, endTime=100.0, dt=0.15):
        self.centredDifferenceH = SWEPC(
            'lakeAtRest-centredDifferenceH',
            output='uq/lakeAtRest-centredDifferenceH',
            testCase='lakeAtRest',
            solver='centredDifferenceH',
            degree=degree,
            elements=elements,
            endTime=endTime,
            dt=dt)

        self.wellBalancedH = SWEPC(
            'lakeAtRest-wellBalancedH',
            output='uq/lakeAtRest-wellBalancedH',
            testCase='lakeAtRest',
            solver='wellBalancedH',
            degree=degree,
            elements=elements,
            endTime=endTime,
            dt=dt)

        self.plot = Gnuplot(
            'lakeAtRest',
            output=os.path.join('uq/lakeatrest'),
            plot=os.path.join('src/uq/lakeatrest.plt'),
            data=self.wellBalancedH.outputs() + 
                 self.centredDifferenceH.outputs())

        self.figure = PDFLaTeXFigure(
            'fig-lakeAtRest',
            output=os.path.join('uq/fig-lakeatrest'),
            figure=os.path.join('src/uq/fig-lakeatrest'),
            components=self.plot.outputs())

    def outputs(self):
        return self.figure.outputs()

    def addTo(self, build):
        build.add(self.centredDifferenceH)
        build.add(self.wellBalancedH)
        build.add(self.plot)
        build.add(self.figure)
