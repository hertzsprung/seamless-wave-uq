#!/usr/bin/env python3
import numpy as np
import matplotlib.pyplot as plt

pos = [1, 2, 5]
data = [np.random.normal(std, std, size=50) for std in pos]

plt.violinplot(data, pos)
plt.show(block=True)
