from env import TrafficLightEnv

env = TrafficLightEnv(False)
done = False

env.reset()

reward_total = 0
while not done:
    obs, reward, terminated, truncated, info = env.step(0)

    reward_total += reward
    
    done = terminated or truncated

env.close()
print(reward_total)
