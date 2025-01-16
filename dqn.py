import gymnasium as gym
import torch
import torch.nn as nn
import numpy as np

env = gym.make("MountainCar-v0", render_mode="human")

term, trunc = True, True
episode = 0
t = 0
while episode < 10000:
    if term or trunc:
        obs, info = env.reset()
        episode += 1

    action = 0
    obs, rew, term, trunc, info = env.step(action)
    if (t := t + 1) % 10 == 0 or obs[0] > 0.4:
        env.render()

env.close()
