import traci
import sumolib
from sumolib import checkBinary
import numpy as np
import gymnasium
from gymnasium import spaces
import time

class TrafficLightEnv(gymnasium.Env):
    def __init__(self):
        super(TrafficLightEnv, self).__init__()
        
        # Define action space (modify phase durations)
        self.action_space = spaces.Discrete(4)  # 4 possible actions
        
        # Define observation space (queue lengths, waiting times, etc.)
        self.observation_space = spaces.Box(
            low=0, high=np.inf, shape=(6,), dtype=np.float32)  # 6 incoming lanes
        
        # Initialize SUMO connection
        self.sumo_cmd = ['sumo-gui', '-c', '../config/three_way.sumocfg']
        traci.start(self.sumo_cmd)
        # Traffic light ID
        self.tl_id = "myTL"

    def reset(self):
        """Reset the environment"""
        traci.close()
        traci.start(self.sumo_cmd)
        return self._get_state()
    
    def close(self):
        """Clean up"""
        traci.close()
# Create environment
env = TrafficLightEnv()

for i in range(100):
    traci.simulationStep()

print(traci.lane.getLastStepVehicleNumber("east_to_center_0"))
        # for lane in ["east_to_center_0", "south_to_center_0", "west_to_center_0"]:
        #     state.append(traci.lane.getLastStepVehicleNumber(lane))
        #     state.append(traci.lane.getWaitingTime(lane))
traci.close()
