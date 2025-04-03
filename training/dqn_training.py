# Import necessary libraries

from stable_baselines3 import DQN
from environment.custom_env import SmartIrrigationEnv
from stable_baselines3.common.evaluation import evaluate_policy

# Create the environment
env = SmartIrrigationEnv()

# Define the DQN model by using Multi-Layer Perceptron policy
dqn_model = DQN(
    "MlpPolicy",
    env,
    learning_rate=0.001,
    gamma=0.99,
    buffer_size=50000,
    batch_size=64,
    exploration_fraction=0.1,
    exploration_final_eps=0.05,
    target_update_interval=100,
    verbose=1,
    tensorboard_log="logs/dqn/"
)

# Evaluate the model before training
mean_reward, _ = evaluate_policy(dqn_model, env, n_eval_episodes=10)
print(f"[DQN] Mean Reward: {mean_reward}")

# Train the agent
dqn_model.learn(total_timesteps=500_000)

# Save the trained model
dqn_model.save("models/dqn/smart_irrigation_dqn")

env.close()

print("DQN training complete. Model saved.")