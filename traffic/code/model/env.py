import traci
import numpy as np
import gymnasium
from gymnasium import spaces
from traci._trafficlight import Phase, Logic

class TrafficLightEnv(gymnasium.Env):
    def __init__(self):
        super(TrafficLightEnv, self).__init__()

        self.tl_id = "myTL"
        
        self.action_space = spaces.Discrete(6)
        self.observation_space = spaces.Box(
            low=0, high=np.inf, shape=(6,), dtype=np.float32)  # 6 incoming lanes
    
        self.sumo_cmd = ['sumo-gui', '-c', '../config/traffic.sumocfg']
        traci.start(self.sumo_cmd)

    def reset(self):
        traci.close()
        traci.start(self.sumo_cmd)
        return self._get_state()
    
    def step(self, action):
        self._apply_action(action)
        

    def _apply_action(self, action):
        logic: Logic = traci.trafficlight.getAllProgramLogics(self.tl_id)[0]
        phases: Phase = logic.phases
        
        if action == 0: 
            phases[0].duration = min(20, phases[0].duration + 1)  
        elif action == 1:  
            phases[2].duration = min(20, phases[2].duration + 1)  
        elif action == 2:  
            phases[4].duration = min(20, phases[4].duration + 1)
        elif action == 3: 
            phases[0].duration = max(5, phases[0].duration - 1) 
        elif action == 4:  
            phases[2].duration = max(5, phases[2].duration - 1)
        elif action == 5:  
            phases[4].duration = max(5, phases[4].duration - 1) 

        logic.phases = phases
        traci.trafficlight.setProgramLogic(self.tl_id, logic)

    def close(self):
        traci.close()

env = TrafficLightEnv()

for i in range(1000):
    traci.simulationStep()


traci.close()
