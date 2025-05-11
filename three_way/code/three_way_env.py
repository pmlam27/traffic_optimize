import traci
import sumolib
from sumolib import checkBinary
import numpy as np
import gymnasium
from gymnasium import spaces

class TrafficLightEnv(gymnasium.Env):
    def __init__(self):
        super(TrafficLightEnv, self).__init__()
        
        # Define action space (modify phase durations)
        self.action_space = spaces.Discrete(6)  # 4 possible actions
        
        # Define observation space (queue lengths, waiting times, etc.)
        self.observation_space = spaces.Box(
            low=0, high=np.inf, shape=(6,), dtype=np.float32)  # 6 incoming lanes
        
        # Initialize SUMO connection
        self.sumo_cmd = ['sumo-gui', '-c', '../config/three_way.sumocfg']
        try:
            traci.start(self.sumo_cmd)
        except traci.exceptions.TraCIException as e:
            print(f"Error starting SUMO: {e}")
            raise
        # traci.start(self.sumo_cmd)
        # Traffic light ID
        self.tl_id = "myTL"

        self.max_waiting_time = 45
        
    def _get_state(self):
        """Get current state of the intersection"""
        state = []
        for lane in ["east_to_center_0", "south_to_center_0", "west_to_center_0"]:
            state.append(traci.lane.getLastStepVehicleNumber(lane))
            state.append(traci.lane.getWaitingTime(lane))
        return np.array(state, dtype=np.float32) 
    
    def step(self, action):
        """Execute one time step within the environment"""
        # Apply action (modify phase timing)
        self._apply_action(action)
        
        # Advance simulation
        traci.simulationStep()
        
        # Get new state
        state = self._get_state()
        
        # Calculate reward
        reward = self._calculate_reward()
        
        # Check if simulation should end
        time = traci.simulation.getTime()
        terminated = time >= 3600  # 1 hour simulation
        truncated = False  # No truncation in this environment
        
        return state, reward, terminated, truncated, {}
    
    def _apply_action(self, action):
        """Modify traffic light timing based on action"""
        phases = traci.trafficlight.getCompleteRedYellowGreenDefinition(self.tl_id)[0].phases
        
            
        if action == 0: 
            phases[0].duration = max(5, phases[0].duration + 5)  # Increase east-west green phase
        elif action == 1:  
            phases[2].duration = max(5, phases[2].duration + 5)  # Increase south-east green phase
        elif action == 2:  
            phases[4].duration = max(5, phases[4].duration + 5)  # Increase west-south green phase
        elif action == 3: 
            phases[0].duration = max(5, phases[0].duration - 5)  # Decrease east-west green phase
        elif action == 4:  
            phases[2].duration = max(5, phases[2].duration - 5)  # Decrease south-east green phase
        elif action == 5:  
            phases[4].duration = max(5, phases[4].duration - 5)  # Decrease west-south green phase
        # Update traffic light program
        logic = traci.trafficlight.Logic("adapted", 0, 0, phases)
        traci.trafficlight.setCompleteRedYellowGreenDefinition(self.tl_id, logic)
    
    def _calculate_reward(self):
        """Calculate reward based on traffic conditions"""
        total_waiting = 0
        max_waiting_penalty = 0
        lanes = ["east_to_center_0", "south_to_center_0", "west_to_center_0"]
        
        for lane in lanes:
            waiting_time = traci.lane.getWaitingTime(lane)
            total_waiting += waiting_time
            
            # Apply penalty if waiting time exceeds the maximum allowed waiting time
            if waiting_time > self.max_waiting_time:
                max_waiting_penalty += waiting_time - self.max_waiting_time
        
        # The reward is negative total waiting time minus the penalty for exceeding max waiting time
        reward = -total_waiting 
        
        return reward

    def reset(self, *, seed=None, options=None):
        """Reset the environment"""
        super().reset(seed=seed)
        traci.close()
        traci.start(self.sumo_cmd)
        return self._get_state(), {}
    
    def close(self):
        """Clean up"""
        traci.close()
