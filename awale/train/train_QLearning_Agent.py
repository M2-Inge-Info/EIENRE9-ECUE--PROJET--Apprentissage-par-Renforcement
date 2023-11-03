# train_QLearning_Agent.py
"""
train_MCTS: Un script pour entraîner un agent qui utilise l'algorithme Monte Carlo Tree Search (MCTS) pour jouer au jeu Awalé.

Auteur: GR Awalé
"""

# Importation des bibliothèques nécessaires
import matplotlib.pyplot as plt
from services.Partie import Partie
import numpy as np

def plot_rewards(total_rewards):
    """
    Fonction pour tracer la récompense totale obtenue à chaque épisode.

    :param total_rewards: Liste des récompenses totales obtenues à chaque épisode.
    """
    # Création du graphique
    plt.figure(figsize=(10, 5))
    plt.plot(total_rewards, label='Récompense par Épisode')
    plt.xlabel('Épisode')
    plt.ylabel('Récompense Totale')
    plt.title('Récompense Totale par Épisode')
    plt.legend()
    plt.show()

def calculate_reward(partie, old_state, new_state):
    """
    Fonction pour calculer la récompense obtenue après un coup.

    :param partie: Instance de la classe Partie représentant l'état actuel du jeu.
    :param old_state: État du jeu avant le coup.
    :param new_state: État du jeu après le coup.
    :return: Récompense calculée.
    """
    # Extraction des scores avant et après le coup
    old_score_joueur1, old_score_joueur2 = old_state[-2:]
    new_score_joueur1, new_score_joueur2 = new_state[-2:]
    diff_score_joueur1 = new_score_joueur1 - old_score_joueur1
    diff_score_joueur2 = new_score_joueur2 - old_score_joueur2
    reward = diff_score_joueur1 - diff_score_joueur2

    # Attribution de récompenses supplémentaires en cas de fin de partie
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
    """
    Fonction pour entraîner l'agent Q-Learning en le faisant jouer contre un agent qui choisit des actions au hasard.

    :param agent: L'agent Q-Learning à entraîner.
    :param env: L'environnement du jeu Awalé.
    :param num_episodes: Nombre de parties à jouer pour l'entraînement.
    :param batch_size: Taille du lot d'expériences à utiliser pour l'apprentissage.
    """
    # Initialisation de la mémoire pour stocker les expériences
    memory = deque(maxlen=50000)
    
    # Boucle sur le nombre d'épisodes
    for episode in range(num_episodes):
        # Initialisation de l'état et de la récompense totale
        state = env.reset()
        total_reward = [0, 0]
        
        # Boucle de jeu jusqu'à la fin de la partie
        while not env.fin:
            # Agent Q-Learning (Joueur 1)
            available_actions = env.get_available_actions()
            action1 = agent.choose_action(state, available_actions)
            old_state = state
            reward = env.coup(action1)
            next_state = env.get_state()
            next_available_actions = env.get_available_actions()
            
            # Enregistrement de l'expérience dans la mémoire
            if reward is not None:
                total_reward[0] += reward
                reward = calculate_reward(env, old_state, next_state)
                memory.append((state, action1, reward, next_state, next_available_actions))
            
            # Vérification de la fin de la partie
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
        
        # Affichage des résultats après chaque épisode
        print(f"Épisode: {episode}, Score: {total_reward}")

def evaluate(agent, env, num_episodes=1000):
    """
    Fonction pour évaluer les performances de l'agent Q-Learning.

    :param agent: L'agent Q-Learning à évaluer.
    :param env: L'environnement du jeu Awalé.
    :param num_episodes: Nombre de parties à jouer pour l'évaluation.
    :return: Taux de victoire de l'agent.
    """
    # Initialisation du compteur de victoires
    wins = 0
    
    # Boucle sur le nombre d'épisodes
    for episode in range(num_episodes):
        # Initialisation de l'état
        state = env.reset()
        
        # Boucle de jeu jusqu'à la fin de la partie
        while not env.fin:
            # Agent Q-Learning (Joueur 1)
            available_actions = env.get_available_actions()
            action1 = agent.choose_action(state, available_actions)
            env.coup(action1)
            
            # Vérification de la fin de la partie et comptage des victoires
            if env.fin:
                if env.vainqueur == 1:
                    wins += 1
                break
            
            # Agent Random (Joueur 2)
            state = env.get_state()
            available_actions = env.get_available_actions()
            action2 = random.choice(available_actions)
            env.coup(action2)
            
    # Calcul et affichage du taux de victoire
    win_rate = wins / num_episodes
    print(f"Taux de victoire: {win_rate * 100:.2f}%")
    return win_rate
