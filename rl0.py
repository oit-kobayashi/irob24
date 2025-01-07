import gymnasium as gym
env = gym.make("CartPole-v1", render_mode="human")

term, trunc = True, True
episode = 0
while episode < 10:
    if term or trunc:
        obs, info = env.reset()
        episode += 1
    action = 1
    obs, rew, term, trunc, info = env.step(action)
env.close()
