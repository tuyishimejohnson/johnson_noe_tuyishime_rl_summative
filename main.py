# Entry point for running experiments
import gym
from stable_baselines3 import DQN, PPO
from environment.rendering_moving import SmartIrrigationEnv, main as render_main

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
    render_main()

# Run simulation for PPO
obs = env.reset()
done = False
while not done:
    action, _states = ppo_model.predict(obs)
    obs, reward, done, info = env.step(action)
    render_main()

env.close()
print("All the simulation completed.")