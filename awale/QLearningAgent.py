from collections import defaultdict, deque
import numpy as np
import random

class QLearningAgent:
    def __init__(self, alpha=0.1, gamma=0.9, epsilon=1.0, epsilon_decay=0.995, epsilon_min=0.01, batch_size=32, memory_size=1000):
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon
        self.epsilon_decay = epsilon_decay
        self.epsilon_min = epsilon_min
        self.Q1 = defaultdict(float)
        self.Q2 = defaultdict(float)
        self.memory = deque(maxlen=memory_size)
        self.batch_size = batch_size

    def choose_action(self, state, available_actions):
        if np.random.uniform(0, 1) < self.epsilon:
            return np.random.choice(available_actions)
        # Average Q-values from both tables
        avg_Q = lambda action: (self.Q1[(state, action)] + self.Q2[(state, action)]) / 2
        return max(available_actions, key=avg_Q)

    def learn(self, state, action, reward, next_state, next_actions):
        self.memory.append((state, action, reward, next_state, next_actions))
        
        if len(self.memory) < self.batch_size:
            return

        batch = random.sample(self.memory, self.batch_size)
        
        for state, action, reward, next_state, next_actions in batch:
            if not next_actions:  # Si next_actions est vide, passez à l'itération suivante
                continue

            if np.random.rand() < 0.5:
                next_max_action = max(next_actions, key=lambda a: self.Q1[(next_state, a)])
                target_Q = reward + self.gamma * self.Q2[(next_state, next_max_action)]
                self.Q1[(state, action)] += self.alpha * (target_Q - self.Q1[(state, action)])
            else:
                next_max_action = max(next_actions, key=lambda a: self.Q2[(next_state, a)])
                target_Q = reward + self.gamma * self.Q1[(next_state, next_max_action)]
                self.Q2[(state, action)] += self.alpha * (target_Q - self.Q2[(state, action)])


        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay
