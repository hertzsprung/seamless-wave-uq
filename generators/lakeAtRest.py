from ninjaopenfoam import Gnuplot, PDFLaTeXFigure, SWEPC
import os

class LakeAtRest:
    def __init__(self, degree=3, elements=100, endTime=10.0, dt=0.15):
        self.centredDifferenceEta = SWEPC(
            'lakeAtRest-centredDifferenceEta',
            output='uq/lakeAtRest-centredDifferenceEta.dat',
            testCase='lakeAtRest',
            solver='centredDifferenceEta',
            degree=degree,
            elements=elements,
            endTime=endTime,
            dt=dt)

        self.wellBalancedH = SWEPC(
            'lakeAtRest-wellBalancedH',
            output='uq/lakeAtRest-wellBalancedH.dat',
            testCase='lakeAtRest',
            solver='wellBalancedH',
            degree=degree,
            elements=elements,
            endTime=endTime,
            dt=dt)

        self.wellBalancedEta = SWEPC(
            'lakeAtRest-wellBalancedEta',
            output='uq/lakeAtRest-wellBalancedEta.dat',
            testCase='lakeAtRest',
            solver='wellBalancedEta',
            degree=degree,
            elements=elements,
            endTime=endTime,
            dt=dt)

        self.plot = Gnuplot(
            'lakeAtRest',
            output=os.path.join('uq/lakeatrest'),
            plot=os.path.join('src/uq/lakeatrest.plt'),
            data=self.wellBalancedEta.outputs() + 
                 self.wellBalancedH.outputs() + 
                 self.centredDifferenceEta.outputs())

        self.figure = PDFLaTeXFigure(
            'fig-lakeAtRest',
            output=os.path.join('uq/fig-lakeatrest'),
            figure=os.path.join('src/uq/fig-lakeatrest'),
            components=self.plot.outputs())

    def outputs(self):
        return self.figure.outputs()

    def addTo(self, build):
        build.add(self.centredDifferenceEta)
        build.add(self.wellBalancedEta)
        build.add(self.wellBalancedH)
        build.add(self.plot)
        build.add(self.figure)
