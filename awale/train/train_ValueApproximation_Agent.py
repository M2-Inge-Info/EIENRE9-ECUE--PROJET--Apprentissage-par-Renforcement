import sys
sys.path.insert(0, '..')

from services.Partie import Partie
from agents.ValueApproximationAgent import ValueFunctionApproximation
from agents.QLearningAgent import QLearningAgent

import random

def advanced_feature_extractor(state_action):
    state, action = state_action
    features = {}

    # Partie de base: Caractéristiques brutes de l'état et de l'action
    for i, seeds in enumerate(state[:-1]):
        features[(f"hole_{i}", seeds)] = 1.0
    features[("action", action)] = 1.0
    features[("player", "player_1" if state[-1] else "player_2")] = 1.0

    # Partie avancée: Statistiques calculées
    # Calculer le nombre total de graines du joueur actuel
    player_seeds = sum(state[:6]) if state[-1] else sum(state[6:12])
    features[("player_seeds", player_seeds)] = 1.0

    # Calculer le nombre de trous vides du joueur actuel
    player_empty_holes = sum(1 for seeds in state[:6] if seeds == 0) if state[-1] else sum(1 for seeds in state[6:12] if seeds == 0)
    features[("player_empty_holes", player_empty_holes)] = 1.0

    # Calculer la différence entre le nombre de graines dans le trou choisi et le nombre moyen de graines par trou pour le joueur actuel
    avg_seeds = player_seeds / 6
    chosen_hole_seeds = state[action]
    seed_diff = chosen_hole_seeds - avg_seeds
    features[("seed_diff", seed_diff)] = 1.0

    # Ajouter d'autres caractéristiques statistiques ou calculées comme vous le jugez pertinent

    return features

# Usage:
state_action = ((4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, True), 5)
features = advanced_feature_extractor(state_action)
print(features)


def train_VFA_Agent(num_games, agent1, agent2):
    for num in range(num_games):
        print(num)

        partie = Partie()  # Initialisez une nouvelle partie
        while not partie.fin:
            state = partie.get_state()
            available_actions = partie.get_available_actions()

            if partie.joueur1:
                action = agent1.choose_action(state, available_actions)
            else:
                action = agent2.choose_action(state, available_actions)  # L'agent aléatoire prend une action aléatoire

            captured_seeds = partie.coup(action)
            reward = partie.get_reward()
            next_state = partie.get_state()
            next_actions = partie.get_available_actions()

            if partie.joueur1:
                agent1.learn(state, action, reward, next_state, next_actions)
        
        if (num + 1) % 10000 == 0:  # Sauvegardez les poids tous les 100 jeux par exemple
            agent1.save_weights(f"agent_weights_game_{num + 1}.pkl")
            print(f"{(num//(num_games//100)) * 5}% achevé")

            
vfa_agent = ValueFunctionApproximation(feature_extractor=advanced_feature_extractor)
# vfa_agent.load_weights("boum.pkl")

agent2 = QLearningAgent()
agent1_file = f"grrr2.pkl"
agent2.load_weights(agent1_file)

# train_VFA_Agent(1000000, vfa_agent, agent2)  # Entraîner l'agent sur 10 000 jeux

def test_VFA_Agent(num_games, agent1, agent2):
    wins = 0
    for num in range(num_games):
        partie = Partie()
        while not partie.fin:
            state = partie.get_state()
            available_actions = partie.get_available_actions()

            if partie.joueur1:
                action = agent1.choose_action(state, available_actions)
            else:
                action = agent2.choose_action(state, available_actions) # L'agent aléatoire prend une action aléatoire

            partie.coup(action)

        if partie.vainqueur == 1:
            wins += 1

    print(f"Agent VFA wins: {wins}/{num_games}")

# # Charger les poids de l'agent si nécessaire
vfa_agent.load_weights("agent_weights_game_310000.pkl")

# # Tester l'agent
test_VFA_Agent(1000, agent2, vfa_agent)  # Tester l'agent sur 1 000 jeux
