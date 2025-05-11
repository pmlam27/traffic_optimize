from stable_baselines3 import PPO  # or DQN, A2C, etc., depending on your model
from three_way_env import TrafficLightEnv
# Load the trained model
model = PPO.load("traffic_light_optimizer.zip")

env = TrafficLightEnv()

# Reset the environment
obs, _ = env.reset()

# Run the simulation for a specified number of steps or until the episode is done
done = False
while not done:
    # Get the action from the model
    action, _states = model.predict(obs, deterministic=True)
    
    # Take a step in the environment
    obs, reward, terminated, truncated, info = env.step(action)
    
    # Check if the episode is done
    done = terminated or truncated

# Close the environment
env.close()
