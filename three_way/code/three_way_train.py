from stable_baselines3 import PPO
from stable_baselines3.common.env_checker import check_env
from three_way_env import TrafficLightEnv

# Create environment
env = TrafficLightEnv()
check_env(env)  # Verify environment follows Gym interface

# Initialize RL model
# model = PPO("MlpPolicy", env, verbose=1)
model = PPO("MlpPolicy", env, verbose=1, learning_rate=0.0003, n_steps=2048, batch_size=64, n_epochs=10)

try:
    # Train the model
    model.learn(total_timesteps=10000)
except Exception as e:
    print(f"An error occurred during training: {e}")
    env.close()  # Ensure the environment is closed properly

# Train the model
# model.learn(total_timesteps=10000)

# Save the model
model.save("traffic_light_optimizer")

env.close()
