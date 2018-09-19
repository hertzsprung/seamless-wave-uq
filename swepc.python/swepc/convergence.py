import numpy as np

class Convergence:
    def __init__(self, flow):
        self.oldWater = np.array(flow.water[:,0])

    def __call__(self, flow):
        sumDiffSquared = 0.0

        for new, old in zip(flow.water[:,0], self.oldWater):
            sumDiffSquared = sumDiffSquared + (new - old)**2

        self.oldWater = np.array(flow.water[:,0])

        return np.sqrt(sumDiffSquared)

