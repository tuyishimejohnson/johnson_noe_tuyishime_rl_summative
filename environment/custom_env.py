import gym
from gym import spaces
import numpy as np

class SmartIrrigationEnv(gym.Env):
    """
    Custom Gym Environment for Smart Irrigation System
    """
    def __init__(self):
        super(SmartIrrigationEnv, self).__init__()
        
        # State space: [Soil Moisture, Weather Forecast, Crop Stage, Water Availability]
        self.observation_space = spaces.MultiDiscrete([3, 3, 4, 4])
        
        # Action space (Discrete: 4 actions)
        self.action_space = spaces.Discrete(4)  # [Full Irrigation, Partial, Delay, Stop]
        
        # Initial state
        self.state = np.array([1, 1, 0, 3])  # Medium Moisture, Dry Weather, Seeding Stage, Sufficient Water
        
        self.done = False
        self.steps = 0
        self.max_steps = 50  # End episode after 50 steps
        
    def step(self, action):
        """
        Executes action and returns new state, reward, done, info
        """
        soil_moisture, weather, crop_stage, water_level = self.state
        reward = 0

        # Define action effects
        if action == 0:  # Full Irrigation
            soil_moisture = min(2, soil_moisture + 2)
            water_level = max(0, water_level - 2)
        elif action == 1:  # Partial Irrigation
            soil_moisture = min(2, soil_moisture + 1)
            water_level = max(0, water_level - 1)
        elif action == 2:  # Delayed Irrigation (No change)
            pass
        elif action == 3:  # Stop Irrigation
            pass

        # Reward Calculation
        if soil_moisture == 1:
            reward = 10  # Optimal irrigation
        elif soil_moisture == 0 or soil_moisture == 2:
            reward = -5  # Over/Under Irrigation
        else:
            reward = -10  # Water wasted or stress

        # Crop Growth Progression
        if self.steps % 10 == 0 and crop_stage < 3:
            crop_stage += 1

        # Check if the episode is over
        if crop_stage == 3 or water_level == 0 or self.steps >= self.max_steps:
            self.done = True

        # Update state
        self.state = np.array([soil_moisture, weather, crop_stage, water_level])
        self.steps += 1
        
        return self.state, reward, self.done, {}
    
    def reset(self):
        """Resets environment to initial state."""
        self.state = np.array([1, 1, 0, 3])  # Reset state
        self.done = False
        self.steps = 0
        return self.state
    
    def render(self, mode='human'):
        """Renders environment state in console (for debugging)."""
        print(f"Soil Moisture: {self.state[0]}, Weather: {self.state[1]}, Crop Stage: {self.state[2]}, Water Level: {self.state[3]}")
    
    def close(self):
        """Closes environment."""
        pass
