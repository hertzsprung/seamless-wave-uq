import numpy as np

class FlowStatistics:
    def __init__(self, flow):
        self.elements = flow.elements
        self.moments = 4

        self.z = np.zeros((self.elements, self.moments))
        self.water = np.zeros((self.elements, self.moments))
        self.q = np.zeros((self.elements, self.moments))

        self.water[:] = [flow.basis.moments(water) for water in flow.water[:]]
        self.q[:] = [flow.basis.moments(q) for q in flow.q[:]]
        self.z[:] = [flow.basis.moments(z) for z in flow.z[:]]
