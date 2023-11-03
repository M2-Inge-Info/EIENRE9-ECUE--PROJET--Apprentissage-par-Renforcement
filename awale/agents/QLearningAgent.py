# QLearningAgent.py
"""
QLearningAgent: Un agent qui utilise l'algorithme Q-Learning pour jouer au jeu Awalé.

Auteur: GR Awalé
"""

import numpy as np
from collections import defaultdict
import pickle


class QLearningAgent:
    """
    Classe représentant un agent utilisant l'algorithme Q-Learning pour prendre des décisions dans le jeu Awalé.
    """

    def __init__(self, alpha=0.05, gamma=0.95, epsilon=0.1, epsilon_decay=0.995):
        """
        Initialise l'agent Q-Learning.

        :param alpha: Taux d'apprentissage.
        :param gamma: Facteur d'escompte.
        :param epsilon: Probabilité d'exploration.
        :param epsilon_decay: Taux de dégradation d'epsilon.
        """
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon
        self.epsilon_min = 0.01
        self.epsilon_decay = epsilon_decay
        self.Q = defaultdict(float)

    def choose_action(self, state, available_actions):
        """
        Choisis une action à partir de l'état actuel en utilisant la politique epsilon-greedy.

        :param state: État actuel du jeu.
        :param available_actions: Actions disponibles dans l'état actuel.
        :return: Action choisie.
        """

        Q_values = [self.Q[(state, a)] for a in available_actions]
        max_Q = max(Q_values)
        return available_actions[np.random.choice([i for i, j in enumerate(Q_values) if j == max_Q])]

    def learn(self, state, action, reward, next_state, next_actions):
        """
        Met à jour la table Q en utilisant l'équation de mise à jour Q-Learning.

        :param state: État actuel.
        :param action: Action effectuée.
        :param reward: Récompense reçue.
        :param next_state: État suivant.
        :param next_actions: Actions disponibles dans l'état suivant.
        """
        max_next_Q = max([self.Q[(next_state, a)] for a in next_actions]) if next_actions else 0
        self.Q[(state, action)] += self.alpha * (reward + self.gamma * max_next_Q - self.Q[(state, action)])
        # if self.epsilon > self.epsilon_min:
        #     self.epsilon *= self.epsilon_decay

    def save(self, filename):
        """
        Sauvegarde la table Q et les paramètres d'epsilon dans un fichier.

        :param filename: Nom du fichier dans lequel sauvegarder les données.
        """
        with open(filename, 'wb') as f:
            pickle.dump((self.Q, self.epsilon), f)

    def load(self, filename):
        """
        Charge la table Q et les paramètres d'epsilon à partir d'un fichier.

        :param filename: Nom du fichier à partir duquel charger les données.
        """
        with open(filename, 'rb') as f:
            self.Q, self.epsilon = pickle.load(f)