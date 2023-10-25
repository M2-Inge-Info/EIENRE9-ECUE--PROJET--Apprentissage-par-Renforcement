from collections import defaultdict, deque
import numpy as np
import random
import pickle

class QLearningAgent:
    def __init__(self, alpha=0.1, gamma=0.9, epsilon=1.0, epsilon_decay=0.995, epsilon_min=0.01, batch_size=32, memory_size=1000, alpha_decay=0.995):
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon
        self.epsilon_decay = epsilon_decay
        self.epsilon_min = epsilon_min
        self.Q1 = defaultdict(float)
        self.Q2 = defaultdict(float)
        self.memory = deque(maxlen=memory_size)
        self.batch_size = batch_size
        self.alpha_decay = alpha_decay
        self.priority_beta = 0.4
        self.priority_epsilon = 1e-6
        self.priorities = defaultdict(float)

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

        # Prioritized Experience Replay
        probabilities = np.array([self.priorities[(state, action)] for state, action, _, _, _ in self.memory])
        total_prob = np.sum(probabilities)

        # Check if total_prob is zero or NaN
        if total_prob == 0 or np.isnan(total_prob):
            # Handle this case, e.g., by setting equal probabilities
            probabilities = np.ones_like(probabilities) / len(self.memory)
        else:
            probabilities /= total_prob

        # Check for NaN values in probabilities
        if np.any(np.isnan(probabilities)):
            print("Warning: NaN values detected in probabilities!")
            probabilities = np.ones_like(probabilities) / len(self.memory)

        batch_indices = np.random.choice(len(self.memory), self.batch_size, p=probabilities)
        batch = [self.memory[i] for i in batch_indices]

        for idx, (state, action, reward, next_state, next_actions) in enumerate(batch):
            if not next_actions:  # Si next_actions est vide, passez à l'itération suivante
                continue

            if np.random.rand() < 0.5:
                next_max_action = max(next_actions, key=lambda a: self.Q1[(next_state, a)])
                target_Q = reward + self.gamma * self.Q2[(next_state, next_max_action)]
                td_error = target_Q - self.Q1[(state, action)]
                self.Q1[(state, action)] += self.alpha * td_error
            else:
                next_max_action = max(next_actions, key=lambda a: self.Q2[(next_state, a)])
                target_Q = reward + self.gamma * self.Q1[(next_state, next_max_action)]
                td_error = target_Q - self.Q2[(state, action)]
                self.Q2[(state, action)] += self.alpha * td_error

            # Update priorities
            self.priorities[(state, action)] = abs(td_error) + self.priority_epsilon

        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay

        # Adaptive Learning Rate
        self.alpha *= self.alpha_decay

    
    def save_weights(self, file_path):
        with open(file_path, 'wb') as file:
            pickle.dump(self.weights, file)
            

    def load_weights(self, file_path):
        with open(file_path, 'rb') as file:
            loaded_weights = pickle.load(file)
            self.weights = loaded_weights