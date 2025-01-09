import gymnasium as gym
env = gym.make("MountainCar-v0", render_mode="human")

Q_RES = 10  # Q関数の解像度(p, v 同じ)
ALPHA = 0.2 # learning rate
GAMMA = 1    # 割引率
q = [[[0, 0, 0] for _ in range(Q_RES)] for _ in range(Q_RES)]

term, trunc = True, True
episode = 0
t = 0
while episode < 10000:
    if term or trunc:
        obs, info = env.reset()
        episode += 1

    p, v = obs[0], obs[1]
    pd = int((p + 1.2) / (0.6 - (-1.2)) * Q_RES)
    vd = int((v + 0.07) / (0.07 - (-0.07)) * Q_RES)
    action = q[pd][vd].index(max(q[pd][vd]))
    obs, rew, term, trunc, info = env.step(action)
    if (t := t + 1) % 10 == 0 or p > 0.4:
        env.render()
    p1, v1 = obs[0], obs[1]
    pd1 = int((p1 + 1.2) / (0.6 - (-1.2)) * Q_RES)
    vd1 = int((v1 + 0.07) / (0.07 - (-0.07)) * Q_RES)

    q[pd][vd][action] += ALPHA * (rew + GAMMA * max(q[pd1][vd1]) - q[pd][vd][action])
    
env.close()
