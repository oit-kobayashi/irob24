# 1/16の授業時からの変更点
# - モデルを変えた (ユニット数増やした)
# - 1バッチの学習回数を増やした
# - その時点でのハイスコア(最右座標)を表示
#
# 時間はかかりますがこれで登ってくれるときは登ります。(ました。)
# ただうまく学習できるかは運任せ的なところもある気もするので
# 皆さんのレポートに期待します。

import gymnasium as gym
import torch
import torch.nn as nn
import numpy as np

env = gym.make("MountainCar-v0", render_mode="human")

model = nn.Sequential(
    nn.Linear(2, 100),
    nn.ReLU(),
     nn.Linear(100, 1000),
    nn.ReLU(),
    nn.Linear(1000, 100),
    nn.ReLU(),
    nn.Linear(100, 3),
)
loss_fn = nn.MSELoss()
opt = torch.optim.Adam(model.parameters())
batch_size = 500
xs = np.array([], dtype=np.float32)
ts = np.array([], dtype=np.float32)

term, trunc = True, True
episode = 0
cnt = 0
xmax = -9
while episode < 10000:
    if term or trunc:
        obs, info = env.reset()
        episode += 1

    y = model(torch.tensor(obs)).detach()
    prob = nn.Softmax(dim=0)(y).numpy()
    action = np.random.choice(3, p=prob)

    obs1, rew, term, trunc, info = env.step(action)
    if obs1[0] > xmax:
        xmax = obs1[0]
        print(xmax)
    t = y.numpy()
    
    t[action] = rew + max(model(torch.tensor(obs1)).detach().numpy())
    xs = np.concatenate((xs.reshape(-1, 2), obs.reshape(-1, 2)))
    ts = np.concatenate((ts.reshape(-1, 3), t.reshape(-1, 3)))
    obs = obs1
    if xs.shape[0] >= batch_size:
        for _ in range(1000):
            y = model(torch.tensor(xs))
            loss = loss_fn(y, torch.tensor(ts))
            opt.zero_grad()
            loss.backward()
            opt.step()
        xs = np.array([], dtype=np.float32)
        ts = np.array([], dtype=np.float32)
        
    if (cnt := cnt + 1) % 100 == 0 or obs[0] > 0.4:
        env.render()

env.close()
