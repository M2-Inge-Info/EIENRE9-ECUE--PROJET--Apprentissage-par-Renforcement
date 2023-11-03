# train_MCTS.py
"""
train_MCTS: Un script pour entraîner l'agent MCTS en le faisant jouer contre un agent qui choisit des actions au hasard.

Auteur: GR Awalé
"""


# Importation des modules nécessaires
from services.Partie import Partie
from agents.MCTSAgent import MCTSAgent
import random

def train_MCTS_Agent(agent, env, num_episodes=1000):
    """
    Fonction pour entraîner l'agent MCTS en le faisant jouer contre un agent qui choisit des actions au hasard.

    Attributs:
        agent (MCTSAgent): L'agent MCTS à entraîner.
        env (Partie): L'environnement du jeu Awalé.
        num_episodes (int): Nombre de parties à jouer pour l'entraînement.

    Méthodes:
        Cette fonction entraîne l'agent MCTS en le faisant jouer contre un agent aléatoire et affiche les résultats.
    """

    # Initialisation du compteur de victoires pour l'agent MCTS, l'agent aléatoire et les égalités
    wins = [0, 0, 0]  # Wins for [Agent MCTS, Agent Random, Draws]
    
    # Boucle sur le nombre d'épisodes
    for episode in range(num_episodes):
        # Réinitialisation de l'environnement du jeu
        state = env.reset()
        
        # Boucle de jeu jusqu'à la fin de la partie
        while not env.fin:
            # Agent MCTS (Joueur 1)
            available_actions = env.get_available_actions()
            action1 = agent.choose_action(state, available_actions)
            env.coup(action1)
            
            # Vérification de la fin de la partie après le coup de l'agent MCTS
            if env.fin:
                break
            
            # Agent Random (Joueur 2)
            state = env.get_state()
            available_actions = env.get_available_actions()
            action2 = random.choice(available_actions)
            env.coup(action2)
        
        # Détermination du vainqueur de la partie
        winner = env.vainqueur
        if winner is not None:
            wins[winner - 1] += 1
        
        # Affichage des résultats après chaque épisode
        print(f"Épisode: {episode}, Vainqueur: {winner}, Victoires cumulatives: MCTS={wins[0]}, Random={wins[1]}, Égalités={wins[2]}")
    
    # Sauvegarde des poids de l'agent après l'entraînement
    agent.save("mcts_agent_weights.pkl")
