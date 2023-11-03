#!/usr/bin/env python3

from tkinter import *

import numpy as np

from agents.QLearningAgent import QLearningAgent
from agents.RandomAgent import RandomAgent
from agents.ValueApproximationAgent import ValueFunctionApproximation
from agents.MCTSAgent import MCTSAgent

from evaluate.evaluate_agents import evaluate_agents

from train.train_QLearning_Agent import train_QLearning_Agent, evaluate
from train.train_MCTS import train_MCTS_Agent

from services.Partie import Partie

import matplotlib.pyplot as plt

import multiprocessing

if __name__ == '__main__':
    agent1 = QLearningAgent()
    # agent1_file = f"gr22.pkl"
    # agent1.load_weights(agent1_file)
    
    # agent2.load_weights(agent1_file)
    
    # scores_joueur1, scores_joueur2 = train_QLearning_Agent(1000, agent1, agent2, 1)
    # print(f"score joeuur 1 {scores_joueur1} - score joueur 2 {scores_joueur2}")
    
    # Création des instances
    env = Partie()
    agent1 = QLearningAgent()
    agent1.load("grrr2.pkl")

    # # Entraînement
    train_QLearning_Agent(agent1, env, 10000, 256)
    evaluate(agent1, env)

    # env = Partie()
    # agentMCTS = MCTSAgent(5000, 10)
    # train_MCTS_Agent(agentMCTS, env, num_episodes=50)
    # # evaluate(agentMCTS, env)
    
    # # evaluate_agent(agent1, 100)
    
    # # Création des agents
    # # agentMCTS = MCTSAgent(num_simulations=1000)
    # agentRandom = RandomAgent()

    # Évaluation des agents
    # evaluate_agents(agentMCTS, agentRandom)
    
    
    
    
# import matplotlib.pyplot as plt

# if __name__ == '__main__':
#     # agent1 = QLearningAgent()
#     # agent1_file = f"gr22.pkl"
#     # agent1.load_weights(agent1_file)
    
#     # agent2 = RandomAgent()
#     # agent2.load_weights(agent1_file)
    
#     # scores_joueur1, scores_joueur2 = train_QLearning_Agent(10000, agent1, agent2, 1)
#     # print(f"score joeuur 1 {scores_joueur1} - score joueur 2 {scores_joueur2}")
    
#     # Création des instances
#     # env = Partie()
#     # agent1 = QLearningAgent()

#     # # Entraînement
#     # train_QLearning_Agent(agent1, env)
#     # evaluate(agent1, env)

#     env = Partie()
#     agentMCTS = MCTSAgent(700, 2)
#     agentMCTS.load("mcts_1_g.pkl")
#     train_MCTS_Agent(agentMCTS, env, num_episodes=5000)
#     # evaluate(agentMCTS, env)
    
#     # evaluate_agent(agent1, 100)
    
#     # Création des agents
#     # agentMCTS = MCTSAgent(num_simulations=1000)
#     agentRandom = RandomAgent()

#     # Évaluation des agents
#     # evaluate_agents(agentMCTS, agentRandom)
    

