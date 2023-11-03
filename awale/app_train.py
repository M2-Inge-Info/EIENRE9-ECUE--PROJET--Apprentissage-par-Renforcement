#!/usr/bin/env python3

from tkinter import *

from agents.ValueApproximationAgent import ValueFunctionApproximation
from agents.QLearningAgent import QLearningAgent
from agents.MCTSAgent import MCTSAgent

from train.train_ValueApproximation_Agent import train_VFA_Agent, test_VFA_Agent, advanced_feature_extractor
from train.train_QLearning_Agent import train_QLearning_Agent, evaluate
from train.train_MCTS import train_MCTS_Agent

from services.Partie import Partie

if __name__ == '__main__':
    env = Partie()
    
    # train du qlearning 
    agent_qlearning_1 = QLearningAgent()
    agent_qlearning_2 = QLearningAgent()
    train_QLearning_Agent(agent_qlearning_1, env, 100000)
    
    # Tester QLearning
    evaluate(agent_qlearning_1, env)
    
    # train du  VFA 
    vfa_agent_1 = ValueFunctionApproximation(feature_extractor=advanced_feature_extractor)
    vfa_agent_2 = ValueFunctionApproximation(feature_extractor=advanced_feature_extractor)
    train_VFA_Agent(100000, vfa_agent_1, vfa_agent_2)  # Entraîner l'agent sur 10 000 jeux
    
    # Tester VFA
    test_VFA_Agent(1000, vfa_agent_1, vfa_agent_2)  # Tester l'agent sur 1 000 jeux
    
    # train du mcts 
    agentMCTS = MCTSAgent(5000, 1.5)
    train_MCTS_Agent(agentMCTS, env, num_episodes=100000)
    
    # Tester du MCTS 
    evaluate(agentMCTS, env)