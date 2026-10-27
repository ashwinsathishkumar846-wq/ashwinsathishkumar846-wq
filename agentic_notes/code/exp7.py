class Environment:
    def __init__(self):
        self.temperature = 28
        self.ac_on = False

    def observe(self):
        return {"temperature": self.temperature, "ac_on": self.ac_on}

    def execute(self, action):
        if action == "turn_on_ac":
            self.ac_on = True
        elif action == "turn_off_ac":
            self.ac_on = False
        self.temperature += -2 if self.ac_on else 3
        return self.temperature


class Agent:
    def __init__(self):
        self.working = {}
        self.episodic = []
        self.semantic = "Temperature above 30 needs cooling"

    def decide(self, obs):
        self.working = dict(obs)
        temp = obs["temperature"]
        if temp > 30:
            print("Knowledge:", self.semantic)
        if temp > 30 and not obs["ac_on"]:
            return "turn_on_ac"
        if temp < 24 and obs["ac_on"]:
            return "turn_off_ac"
        return "wait"

    def remember(self, obs, action, new_temp):
        self.episodic.append((obs, action, new_temp))


env = Environment()
agent = Agent()

print("=== CoALA Cognitive Agent ===")

for step in range(1, 10):
    obs = env.observe()
    print("Step:", step, "| Observation:", obs)
    action = agent.decide(obs)
    new_temp = env.execute(action)
    agent.remember(obs, action, new_temp)
    print("Action:", action, "| New temperature:", new_temp)
    print()

print("Episodic memory:", len(agent.episodic), "episodes")
