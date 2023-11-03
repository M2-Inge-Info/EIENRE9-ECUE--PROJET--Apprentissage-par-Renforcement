import numpy as np
from agents.MCTSAgent import MCTSAgent
from agents.RandomAgent import RandomAgent
from services.Partie import Partie

def evaluate_agents(agent1, agent2, num_episodes=100):
    env = Partie()
    wins = {1: 0, 2: 0, 0: 0}  # 0 pour les égalités

    for episode in range(num_episodes):
        state = env.reset()
        done = False

        while not done:
            if env.joueur1:
                action = agent1.choose_action(state, env.get_available_actions())
            else:
                action = agent2.choose_action(state, env.get_available_actions())

            gain = env.coup(action)
            next_state = env.get_state()
            done = env.fin

            state = next_state

        wins[env.vainqueur] += 1

    print(f"Agent 1 wins: {wins[1]}, Agent 2 wins: {wins[2]}, Draws: {wins[0]}")



