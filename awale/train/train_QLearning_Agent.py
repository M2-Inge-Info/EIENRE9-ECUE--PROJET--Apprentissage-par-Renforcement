import matplotlib.pyplot as plt
from services.Partie import Partie
import numpy as np

def plot_rewards(total_rewards):
    plt.figure(figsize=(10, 5))
    plt.plot(total_rewards, label='Récompense par Épisode')
    plt.xlabel('Épisode')
    plt.ylabel('Récompense Totale')
    plt.title('Récompense Totale par Épisode')
    plt.legend()
    plt.show()

def calculate_reward(partie, old_state, new_state):
    old_score_joueur1, old_score_joueur2 = old_state[-2:]
    new_score_joueur1, new_score_joueur2 = new_state[-2:]
    diff_score_joueur1 = new_score_joueur1 - old_score_joueur1
    diff_score_joueur2 = new_score_joueur2 - old_score_joueur2
    reward = diff_score_joueur1 - diff_score_joueur2

    if partie.fin:
        if partie.vainqueur == 1:
            reward += 10
        elif partie.vainqueur == 2:
            reward -= 10
        else:
            reward += 5

    return reward

from collections import deque
import random

def train_QLearning_Agent(agent, env, num_episodes=10000, batch_size=128):
    memory = deque(maxlen=50000)
    
    for episode in range(num_episodes):
        state = env.reset()
        total_reward = [0, 0]
        
        while not env.fin:
            # Agent Q-Learning (Joueur 1)
            available_actions = env.get_available_actions()
            action1 = agent.choose_action(state, available_actions)
            old_state = state
            reward = env.coup(action1)
            next_state = env.get_state()
            next_available_actions = env.get_available_actions()
            
            if reward is not None:
                total_reward[0] += reward
                reward = calculate_reward(env, old_state, next_state)
                memory.append((state, action1, reward, next_state, next_available_actions))
            
            if env.fin:
                break
            
            # Agent Random (Joueur 2)
            state = next_state
            available_actions = env.get_available_actions()
            action2 = random.choice(available_actions)
            reward = env.coup(action2)
            if reward is not None:
                total_reward[1] += reward
        
        # Experience Replay
        if len(memory) >= batch_size:
            minibatch = random.sample(memory, batch_size)
            for state, action, reward, next_state, next_actions in minibatch:
                agent.learn(state, action, reward, next_state, next_actions)
        
        print(f"Épisode: {episode}, Score: {total_reward}")

def evaluate(agent, env, num_episodes=1000):
    wins = 0
    for episode in range(num_episodes):
        state = env.reset()
        while not env.fin:
            # Agent Q-Learning (Joueur 1)
            available_actions = env.get_available_actions()
            action1 = agent.choose_action(state, available_actions)
            env.coup(action1)
            
            if env.fin:
                if env.vainqueur == 1:
                    wins += 1
                break
            
            # Agent Random (Joueur 2)
            state = env.get_state()
            available_actions = env.get_available_actions()
            action2 = random.choice(available_actions)
            env.coup(action2)
            
    win_rate = wins / num_episodes
    print(f"Taux de victoire: {win_rate * 100:.2f}%")
    return win_rate

