import gym
import torch
from stable_baselines3 import DQN
from environment.custom_env import SmartIrrigationEnv

# Create the environment
env = SmartIrrigationEnv()

# Define the DQN model
model = DQN(
    "MlpPolicy",  # Use a Multi-Layer Perceptron policy
    env,
    learning_rate=0.001,  # Adjust learning rate
    gamma=0.99,  # Discount factor
    buffer_size=50000,  # Replay buffer size
    batch_size=32,  # Mini-batch size
    exploration_fraction=0.1,  # Fraction of training steps for exploration
    exploration_final_eps=0.05,  # Final exploration rate
    target_update_interval=100,  # Target network update frequency
    verbose=1,
    tensorboard_log="logs/dqn/"
)

# Train the agent
model.learn(total_timesteps=50000)

# Save the trained model
model.save("models/dqn/smart_irrigation_dqn")

env.close()

print("DQN training complete. Model saved.")
