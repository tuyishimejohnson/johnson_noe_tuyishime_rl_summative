# Smart Irrigation RL

This project simulates a smart irrigation system using reinforcement learning algorithms. The environment models soil conditions, weather, crop growth stages, and water levels, while agents are trained using DQN and PPO to optimize irrigation strategies.

## Project Structure

- `environment/` - Contains the custom Gym environment and visualization tools.
- `training/` - Training scripts for DQN and PPO models.
- `models/` - Directory for storing trained models.
- `main.py` - Script for running and evaluating trained models.


## Requirements

- Python 3.8+
- Required Python packages:
  - `gym`
  - `numpy`
  - `stable-baselines3`
  - `PyOpenGL` (for rendering)

Use this command to install dependencies: 

`pip install -r requirements.txt`