from stable_baselines3 import PPO  # or DQN, A2C, etc., depending on your model
from env import TrafficLightEnv
import matplotlib.pyplot as plt
import traci
# Load the trained model
model = PPO.load("output/traffic_light_optimizer_mk2.zip")

env = TrafficLightEnv(False)

obs, _ = env.reset()

times = []
vehicle_counts = []
vehicle_counts2 = []

done = False

reward_total = 0
while not done:
    action, _states = model.predict(obs, deterministic=True)
    print(f"Action: {action}")
    
    obs, reward, terminated, truncated, info = env.step(action)

    reward_total += reward

    times.append(env.get_time())
    vehicle_counts.append(obs.sum())
    
    done = terminated or truncated

env.close()
print(reward_total)
reward_total = 0

# sumo_cmd = ['sumo', '-c', '../../config/traffic.sumocfg']
# traci.start(sumo_cmd)

# hourly_sum = 0

# for i in range(24100):
#     if (i % 300 == 0):
#         vehicle_counts2.append(hourly_sum)
#         hourly_sum = 0
#     else:
#         hourly_sum += traci.lane.getLastStepVehicleNumber("east_to_center_0")
#         hourly_sum += traci.lane.getLastStepVehicleNumber("south_to_center_0")
#         hourly_sum += traci.lane.getLastStepVehicleNumber("west_to_center_0")
#     traci.simulationStep()

# traci.close()

# Plot the result
plt.figure(figsize=(10, 5))
plt.plot(times, vehicle_counts, marker='o', linestyle='-', color='blue')
# plt.plot(times, vehicle_counts2, marker='o', linestyle='-', color='red')
plt.title("Number of Vehicles on the Road vs. Time")
plt.xlabel("Simulation Step (time)")
plt.ylabel("Number of Vehicles")
plt.grid(True)
plt.savefig("vehicle_count_plot.png")

plt.show()
