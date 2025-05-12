import matplotlib.pyplot as plt
import traci
import subprocess

subprocess.run(["/home/pmlam/Workspaces/sumo_ws/traffic_optimize/traffic/route/generate_trip.sh"])

sumo_cmd = ['sumo-gui', '-c', '../../config/traffic.sumocfg']
traci.start(sumo_cmd)

times = []
vehicle_counts = []

hourly_sum = 0

for i in range(24100):
    if (i % 300 == 0):
        times.append(i)
        vehicle_counts.append(hourly_sum / 300)
        hourly_sum = 0
    else:
        hourly_sum += traci.lane.getWaitingTime("west_to_center_0")
    traci.simulationStep()

traci.close()

# Plot the result
plt.figure(figsize=(10, 5))
plt.plot(times, vehicle_counts, marker='o', linestyle='-')
plt.title("Number of Vehicles on the Road vs. Time")
plt.xlabel("Simulation Step (time)")
plt.ylabel("Number of Vehicles")
plt.grid(True)
plt.savefig("vehicle_count_plot.png")

plt.show()
