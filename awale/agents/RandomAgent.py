# RandomAgent.py
"""
RandomAgent: Un agent qui choisit des actions au hasard.

Auteur: GR Awalé
"""

import numpy as np

class RandomAgent:
    """
    Classe représentant un agent qui choisit des actions au hasard.

    Attributs:
        Aucun attribut nécessaire pour cet agent.

    Méthodes:
        - choose_action: Sélectionne une action au hasard parmi les actions disponibles.
        - learn: L'agent aléatoire ne réalise pas d'apprentissage, donc cette méthode ne fait rien.
    """

    def __init__(self):
        """
        Initialise l'agent aléatoire.
        """
        pass

    def choose_action(self, state, available_actions):
        """
        Choisis une action au hasard parmi les actions disponibles.

        :param state: État actuel du jeu (non utilisé par cet agent).
        :param available_actions: Liste des actions disponibles.
        :return: Une action choisie au hasard.
        """
        return np.random.choice(available_actions)

    def learn(self, state, action, reward, next_state, next_actions):
        """
        L'agent aléatoire ne réalise pas d'apprentissage, donc cette méthode ne fait rien.

        :param state: État actuel du jeu.
        :param action: Action effectuée.
        :param reward: Récompense reçue.
        :param next_state: État suivant du jeu.
        :param next_actions: Actions disponibles dans l'état suivant.
        """
        pass
