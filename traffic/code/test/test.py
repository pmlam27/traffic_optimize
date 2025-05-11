import matplotlib.pyplot as plt
import traci

sumo_cmd = ['sumo-gui', '-c', '../../config/traffic.sumocfg']
traci.start(sumo_cmd)

times = []
vehicle_counts = []

hourly_sum = 0

for i in range(24100):
    if (i % 100 == 0):
        times.append(i)
        vehicle_counts.append(hourly_sum)
        hourly_sum = 0
    else:
        hourly_sum += len(traci.vehicle.getIDList())

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
