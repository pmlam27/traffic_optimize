from stable_baselines3 import PPO
from stable_baselines3.common.env_checker import check_env
from env import TrafficLightEnv

print("Checking environment...")
# Create environment
env = TrafficLightEnv(False)
# check_env(env)  # Verify environment follows Gym interface

print("Environment check complete.")
# Initialize RL model
# model = PPO("MlpPolicy", env, verbose=1)
# model = PPO("MlpPolicy", env, verbose=1, learning_rate=0.0003, n_steps=1024, batch_size=64, n_epochs=10)
model = PPO.load("output/traffic_light_optimizer_mk2.zip", env=env)
# model.env = env
model.device = "cuda"

# Train the model
model.learn(total_timesteps=10000)

# Train the model
# model.learn(total_timesteps=10000)

# Save the model
model.save("output/traffic_light_optimizer_mk2")

env.close()
