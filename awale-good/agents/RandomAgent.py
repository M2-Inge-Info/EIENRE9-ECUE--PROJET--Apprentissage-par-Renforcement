import numpy as np

class RandomAgent:
    def __init__(self):
        pass

    def choose_action(self, state, available_actions):
        return np.random.choice(available_actions)

    def learn(self, state, action, reward, next_state, next_actions):
        # L'agent aléatoire n'apprend pas, donc cette méthode ne fait rien.
        pass
