import gym
from stable_baselines3 import PPO
from stable_baselines3.common.env_util import make_vec_env
from stable_baselines3.common.evaluation import evaluate_policy
from environment.custom_env import SmartIrrigationEnv

env = SmartIrrigationEnv()

# Create and train PPO model
ppo_model = PPO(
    "MlpPolicy",
    env,
    learning_rate=5e-4,
    gamma=0.99,
    n_steps=128,
    batch_size=64,
    verbose=1,
    tensorboard_log="/logs/ppo/"
)

ppo_model.learn(total_timesteps=500_000)
ppo_model.save("models/pg/ppo_smart_irrigation")

# Evaluate
mean_reward, _ = evaluate_policy(ppo_model, env, n_eval_episodes=10)
print(f"[PPO] Mean Reward: {mean_reward}")

env.close()

print("PPO training complete. Model saved.")