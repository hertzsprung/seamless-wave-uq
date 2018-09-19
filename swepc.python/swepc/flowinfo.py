import numpy as np

class FlowInfoEta:
    def __init__(self, g):
        self.g = g

    def maxWaveSpeed(self, flow):
        v = 0.0
        for i in range(flow.elements):
            h = flow.water[i,0] - flow.z[i,0]
            v = max(v, abs(flow.q[i,0] / h) + np.sqrt(self.g*h))
        return v

class FlowInfoH:
    def __init__(self, g):
        self.g = g

    def maxWaveSpeed(self, flow):
        v = 0.0
        for i in range(flow.elements):
            h = flow.water[i,0]
            v = max(v, abs(flow.q[i,0] / h) + np.sqrt(self.g*h))
        return v
