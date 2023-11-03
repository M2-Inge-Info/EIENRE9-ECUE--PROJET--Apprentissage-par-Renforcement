# train_ValueApproxmation_Agent.py
"""
train_MCTS: Un script pour entraîner un agent utilisant l'approximation de la fonction de valeur.

Auteur: GR Awalé
"""

# Importation des bibliothèques et modules nécessaires
import sys
sys.path.insert(0, '..')
from services.Partie import Partie
from agents.ValueApproximationAgent import ValueFunctionApproximation
from agents.QLearningAgent import QLearningAgent
import random

def advanced_feature_extractor(state_action):
    """
    Fonction pour extraire des caractéristiques avancées à partir d'un état et d'une action.

    :param state_action: Tuple contenant l'état du jeu et l'action à effectuer.
    :return: Dictionnaire contenant les caractéristiques extraites.
    """
    # Extraction de l'état et de l'action
    state, action = state_action
    features = {}

    # Caractéristiques brutes de l'état et de l'action
    for i, seeds in enumerate(state[:-1]):
        features[(f"hole_{i}", seeds)] = 1.0
    features[("action", action)] = 1.0
    features[("player", "player_1" if state[-1] else "player_2")] = 1.0

    # Statistiques calculées
    player_seeds = sum(state[:6]) if state[-1] else sum(state[6:12])
    features[("player_seeds", player_seeds)] = 1.0

    player_empty_holes = sum(1 for seeds in state[:6] if seeds == 0) if state[-1] else sum(1 for seeds in state[6:12] if seeds == 0)
    features[("player_empty_holes", player_empty_holes)] = 1.0

    avg_seeds = player_seeds / 6
    chosen_hole_seeds = state[action]
    seed_diff = chosen_hole_seeds - avg_seeds
    features[("seed_diff", seed_diff)] = 1.0

    # Ajout d'autres caractéristiques statistiques ou calculées si nécessaire

    return features

def train_VFA_Agent(num_games, agent1, agent2):
    """
    Fonction pour entraîner un agent utilisant l'approximation de la fonction de valeur.

    :param num_games: Nombre de parties à jouer pour l'entraînement.
    :param agent1: Agent à entraîner.
    :param agent2: Agent adversaire.
    """
    for num in range(num_games):
        print(num)

        partie = Partie()  # Initialisation d'une nouvelle partie
        while not partie.fin:
            state = partie.get_state()
            available_actions = partie.get_available_actions()

            if partie.joueur1:
                action = agent1.choose_action(state, available_actions)
            else:
                action = agent2.choose_action(state, available_actions)

            captured_seeds = partie.coup(action)
            reward = partie.get_reward()
            next_state = partie.get_state()
            next_actions = partie.get_available_actions()

            if partie.joueur1:
                agent1.learn(state, action, reward, next_state, next_actions)
        
        # Sauvegarde des poids de l'agent périodiquement
        if (num + 1) % 500 == 0:
            agent1.save_weights(f"agent_VFA_{num + 1}.pkl")
            print(f"{(num//(num_games//100)) * 5}% achevé")

def test_VFA_Agent(num_games, agent1, agent2):
    """
    Fonction pour tester les performances de l'agent utilisant l'approximation de la fonction de valeur.

    :param num_games: Nombre de parties à jouer pour le test.
    :param agent1: Agent à tester.
    :param agent2: Agent adversaire.
    """
    wins = 0
    for num in range(num_games):
        partie = Partie()
        while not partie.fin:
            state = partie.get_state()
            available_actions = partie.get_available_actions()

            if partie.joueur1:
                action = agent1.choose_action(state, available_actions)
            else:
                action = agent2.choose_action(state, available_actions)

            partie.coup(action)

        if partie.vainqueur == 1:
            wins += 1

    # Affichage des résultats du test
    print(f"Agent VFA wins: {wins}/{num_games}")

# Initialisation des agents et entraînement
# vfa_agent_1 = ValueFunctionApproximation(feature_extractor=advanced_feature_extractor)
# vfa_agent_2 = ValueFunctionApproximation(feature_extractor=advanced_feature_extractor)
# train_VFA_Agent(50000, vfa_agent_1, vfa_agent_2)  # Entraîner l'agent sur 10 000 jeux

# Tester l'agent
# test_VFA_Agent(1000, vfa_agent_1, vfa_agent_2)  # Tester l'agent sur 1 000 jeux

""""
37% -> 67% 
Agent VFA wins: 670/1000
"""