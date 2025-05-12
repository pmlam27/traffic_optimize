import traci
import numpy as np
import gymnasium
from gymnasium import spaces
from traci._trafficlight import Phase, Logic
import subprocess

class TrafficLightEnv(gymnasium.Env):
    def __init__(self, enable_gui=True):
        super(TrafficLightEnv, self).__init__()
        self.tl_id = "myTL"
        
        self.action_space = spaces.Discrete(7)
        self.observation_space = spaces.Box(
            low=0, high=np.inf, shape=(4,), dtype=np.float32) 
        if enable_gui:
            self.sumo_cmd = ['sumo-gui', '-c', '../../config/traffic.sumocfg']
        else:
            self.sumo_cmd = ['sumo', '-c', '../../config/traffic.sumocfg']
        traci.start(self.sumo_cmd)

    def reset(self, seed=None, options=None):
        print("Resetting TrafficLightEnv...")
        print("reset random trips ...")
        subprocess.run(["/home/pmlam/Workspaces/sumo_ws/traffic_optimize/traffic/route/generate_trip.sh"])

        super().reset(seed=seed)
        traci.close()
        traci.start(self.sumo_cmd)
        return np.array([0, 0, 0, 0], dtype=np.float32) , {}
    
    def step(self, action):
        self._apply_action(action)

        lane1, lane2, lane3 = 0, 0, 0

        for i in range(300):
            traci.simulationStep()
            lane1 += traci.lane.getWaitingTime("east_to_center_0")
            lane2 += traci.lane.getWaitingTime("south_to_center_0")
            lane3 += traci.lane.getWaitingTime("west_to_center_0")
        
        state = np.array([lane1, lane2, lane3, traci.simulation.getTime()], dtype=np.float32) 

        reward = 0

        lane1_norm = lane1 / 300
        lane2_norm = lane2 / 300
        lane3_norm = lane3 / 300

        if lane1_norm > 50:
            reward -= (lane1_norm - 50)

        if lane2_norm > 50:
            reward -= (lane2_norm - 50)
        
        if lane3_norm > 50:
            reward -= (lane3_norm - 50)

        time = traci.simulation.getTime()
        terminated = time >= 24100
        truncated = False
        info = {}
        return state, reward, terminated, truncated, info
    

    def _apply_action(self, action):
        logic: Logic = traci.trafficlight.getAllProgramLogics(self.tl_id)[0]
        phases: Phase = logic.phases
        
        if action == 0:
            phases[0].duration = 20
            phases[2].duration = 20
            phases[4].duration = 20
        elif action == 1: 
            phases[0].duration = 50
            phases[2].duration = 10
            phases[4].duration = 10
        elif action == 2:  
            phases[0].duration = 10
            phases[2].duration = 50
            phases[4].duration = 10
        elif action == 3:  
            phases[0].duration = 10
            phases[2].duration = 10
            phases[4].duration = 50
        elif action == 4: 
            phases[0].duration = 40
            phases[2].duration = 40
            phases[4].duration = 10
        elif action == 5:  
            phases[0].duration = 40
            phases[2].duration = 10
            phases[4].duration = 40
        elif action == 6:  
            phases[0].duration = 10
            phases[2].duration = 40
            phases[4].duration = 40

        logic.phases = phases
        traci.trafficlight.setProgramLogic(self.tl_id, logic)

    def close(self):
        print("Closing TrafficLightEnv...")
        traci.close()

    def get_time(self):
        return traci.simulation.getTime()
    

# env = TrafficLightEnv()

# for i in range(1000):
#     traci.simulationStep()


# traci.close()
