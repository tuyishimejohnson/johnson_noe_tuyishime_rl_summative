import gym
from gym import spaces
import numpy as np

class SmartIrrigationEnv(gym.Env):
    def __init__(self):
        super(SmartIrrigationEnv, self).__init__()

        # State space: Soil Moisture, Weather, Crop Stage, Water Availability
        self.observation_space = spaces.MultiDiscrete([3, 3, 4, 4])
        
        # Actions: Full, Partial, Delay, Stop
        self.action_space = spaces.Discrete(4)

        # Initial state
        self.state = np.array([1, 1, 0, 3])  # Medium Moisture, Dry, Seeding, Sufficient Water
        self.steps = 0
        self.max_steps = 50
        self.done = False

    def step(self, action):
        soil, weather, stage, water = self.state
        reward = 0

        # Action effects
        if action == 0:  # Full
            soil = min(2, soil + 2)
            water = max(0, water - 2)
        elif action == 1:  # Partial
            soil = min(2, soil + 1)
            water = max(0, water - 1)
        elif action == 2:  # Delay
            soil = max(0, soil - 1) if weather == 1 else soil  # dry weather causes loss
        elif action == 3:  # Stop
            soil = max(0, soil - 1)

        # Reward logic
        if soil == 1:
            reward = 10
        elif soil == 0 or soil == 2:
            reward = -5
        else:
            reward = -10

        # Crop progression every 10 steps
        if self.steps % 10 == 0 and stage < 3:
            stage += 1

        # Terminal Conditions
        if water == 0 or stage == 3 or self.steps >= self.max_steps:
            self.done = True

        self.state = np.array([soil, weather, stage, water])
        self.steps += 1

        return self.state, reward, self.done, {}

    def reset(self):
        self.state = np.array([1, 1, 0, 3])
        self.steps = 0
        self.done = False
        return self.state

    def render(self, mode='human'):
        soil, weather, stage, water = self.state
        print(f"Step {self.steps} | Soil: {soil}, Weather: {weather}, Stage: {stage}, Water: {water}")

    def close(self):
        pass