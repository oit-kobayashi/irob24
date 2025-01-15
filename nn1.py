import torch
import torch.nn as nn
import numpy as np
import matplotlib.pyplot as plt

N = 5000
x = np.random.random((N, 2)).astype(np.float32) * 6 - 3

_x = x * x * np.array([1/4, 1])
_x2 = x * x * np.array([2, 2])
tf = np.logical_and(
    _x[:, 0] + _x[:, 1] < 1,
    _x2[:, 0] + _x2[:, 1] > 1
)

y = np.zeros((N, 2))
y[tf == True] = [0, 1]
y[tf != True] = [1, 0]

xt = torch.from_numpy(x)
yt = torch.from_numpy(y)

model = nn.Sequential(
    nn.Linear(2, 10),
    nn.ReLU(),

    nn.Linear(10, 10),
    nn.ReLU(),

    nn.Linear(10, 10),
    nn.ReLU(),

    nn.Linear(10, 2),
    nn.Softmax(dim=1)
)

loss_fn = nn.CrossEntropyLoss()
opt = torch.optim.Adam(model.parameters())

pred = model(xt)
loss = loss_fn(pred, yt)
print(loss)

for _ in range(2000):
    pred = model(xt)
    loss = loss_fn(pred, yt)
    opt.zero_grad()
    loss.backward()
    opt.step()

print(loss)
tf2 = pred[:, 0] < pred[:, 1]

plt.subplot(1, 2, 1)
plt.scatter(x[tf, 0], x[tf, 1], s=10)
plt.scatter(x[tf != True, 0], x[tf != True, 1], s=10)
plt.subplot(1, 2, 2)
plt.scatter(x[tf2, 0], x[tf2, 1], s=10)
plt.scatter(x[tf2 != True, 0], x[tf2 != True, 1], s=10)


plt.show()

