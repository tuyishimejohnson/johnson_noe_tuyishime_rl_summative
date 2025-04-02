# Entry point for running experiments
import gym
from stable_baselines3 import DQN, PPO
from environment.custom_env import SmartIrrigationEnv

# Load environment
env = SmartIrrigationEnv()

# Load trained models
dqn_model = DQN.load("models/dqn/smart_irrigation_dqn", env)
ppo_model = PPO.load("models/pg/ppo_smart_irrigation", env)

# Run simulation for DQN
obs = env.reset()
done = False
while not done:
    action, _states = dqn_model.predict(obs)
    obs, reward, done, info = env.step(action)
    env.render()

# Run simulation for PPO
obs = env.reset()
done = False
while not done:
    action, _states = ppo_model.predict(obs)
    obs, reward, done, info = env.step(action)
    env.render()

env.close()
print("All the simulation completed.")