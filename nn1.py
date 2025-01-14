import torch
import torch.nn as nn
import numpy as np
import matplotlib.pyplot as plt

N = 1000
x = np.random.random((N, 2)).astype(np.float32) * 6 - 3

_x = x * x * np.array([1/4, 1])
tf = _x[:, 0] + _x[:, 1] < 1

# y = np.zeros((N, 2))
# y[tf == True] = [0, 1]
# y[tf != True] = [1, 0]

plt.scatter(x[tf, 0], x[tf, 1], s=10)
plt.scatter(x[tf!=True, 0], x[tf!=True, 1], s=10)
plt.show()

