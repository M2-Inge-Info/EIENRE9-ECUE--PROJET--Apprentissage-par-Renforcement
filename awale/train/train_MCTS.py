# train_MCTS.py
from services.Partie import Partie
from agents.MCTSAgent import MCTSAgent
import random

def train_MCTS_Agent(agent, env, num_episodes=1000):
    wins = [0, 0, 0]  # Wins for [Agent MCTS, Agent Random, Draws]
    
    for episode in range(num_episodes):
        state = env.reset()
        
        while not env.fin:
            # Agent MCTS (Joueur 1)
            available_actions = env.get_available_actions()
            action1 = agent.choose_action(state, available_actions)
            env.coup(action1)
            
            if env.fin:
                break
            
            # Agent Random (Joueur 2)
            state = env.get_state()
            available_actions = env.get_available_actions()
            action2 = random.choice(available_actions)
            env.coup(action2)
        
        # Determine the winner
        winner = env.vainqueur
        if winner is not None:
            wins[winner - 1] += 1
        
        print(f"Épisode: {episode}, Vainqueur: {winner}, Victoires cumulatives: MCTS={wins[0]}, Random={wins[1]}, Égalités={wins[2]}")
    # Save the agent's weights
    agent.save("mcts_agent_weights.pkl")