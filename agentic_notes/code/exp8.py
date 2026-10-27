import gymnasium as gym
from gymnasium import spaces


class GridWorldEnv(gym.Env):
    def __init__(self):
        super().__init__()
        self.observation_space = spaces.Discrete(16)
        self.action_space = spaces.Discrete(4)
        self.state = 0
        self.steps = 0

    def reset(self, seed=None, options=None):
        super().reset(seed=seed)
        self.state = 0
        self.steps = 0
        return self.state, {}

    def step(self, action):
        row, col = divmod(self.state, 4)
        if action == 0:
            row = max(row - 1, 0)
        elif action == 1:
            row = min(row + 1, 3)
        elif action == 2:
            col = max(col - 1, 0)
        else:
            col = min(col + 1, 3)
        self.state = row * 4 + col
        self.steps += 1
        terminated = self.state == 15
        reward = 10.0 if terminated else -0.1
        return self.state, reward, terminated, False, {}


env = GridWorldEnv()
names = {0: "Up", 1: "Down", 2: "Left", 3: "Right"}
state, _ = env.reset()
print("Observation space:", env.observation_space)
print("Action space:", env.action_space)
print("Start state:", state)

total = 0
for action in [3, 3, 3, 1, 1, 1]:
    state, reward, terminated, truncated, _ = env.step(action)
    total += reward
    print("Action:", names[action], "State:", state,
          "Reward:", reward, "Terminated:", terminated)
    if terminated:
        break

print("Total reward:", round(total, 2))
