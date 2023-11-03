# MCTSAgent.py
"""
MCTSAgent: Un agent qui utilise l'algorithme Monte Carlo Tree Search (MCTS) pour jouer au jeu Awalé.

Auteur: GR Awalé
"""

import numpy as np
import random
from collections import defaultdict
from services.Partie import Partie
import pickle


class MCTSAgent:
    """
    Classe représentant un agent utilisant l'algorithme MCTS pour prendre des décisions dans le jeu Awalé.
    """

    def __init__(self, num_simulations=8000, exploration_weight=1.25):
        """
        Initialise l'agent MCTS.

        :param num_simulations: Nombre de simulations à effectuer pour chaque action possible.
        :param exploration_weight: Poids donné à l'exploration dans la formule UCB.
        """
        self.num_simulations = num_simulations
        self.exploration_weight = exploration_weight
        self.Q = defaultdict(float)  # Total reward of each (state, action)
        self.N = defaultdict(int)    # Total visit count of each (state, action)

    def choose_action(self, state, available_actions):
        """
        Choisis une action à partir de l'état actuel en utilisant MCTS.

        :param state: État actuel du jeu.
        :param available_actions: Actions disponibles dans l'état actuel.
        :return: Action choisie.
        """
        available_actions = self.preprocess_actions(state, available_actions)
        for _ in range(self.num_simulations):
            self.simulate(state, available_actions)
        
        # Select action based on UCB formula
        ucb_values = [(self.Q[(state, a)] / (1 + self.N[(state, a)]) +
                       self.exploration_weight * np.sqrt(np.log(sum(self.N[(state, a)] for a in available_actions) + 1e-10) / (1 + self.N[(state, a)] + 1e-10)))
                      for a in available_actions]
        return available_actions[np.argmax(ucb_values)]
    
    def preprocess_actions(self, state, available_actions):
        """
        Pré-traite les actions disponibles en utilisant une heuristique.

        :param state: État actuel du jeu.
        :param available_actions: Actions disponibles dans l'état actuel.
        :return: Actions pré-traitées.
        """
        return [action for action in available_actions if self.estimate_gain(state, action) >= 0]

    def simulate(self, state, available_actions):
        """
        Simule une partie à partir de l'état actuel et met à jour les valeurs Q et N.

        :param state: État actuel du jeu.
        :param available_actions: Actions disponibles dans l'état actuel.
        """
        env = Partie()
        env.liste, env.joueur1, env.score = list(state[:-1]), state[-1], [0, 0]
        path = []
        done = False
        
        # Selection and Expansion
        while not done:
            action = self.rollout_policy(state, available_actions)
            reward = env.coup(action)
            state = env.get_state()
            available_actions = env.get_available_actions()
            done = env.fin
        
        # Ensure reward is a number
        reward = reward if reward is not None else 0
        
        # Backpropagation
        for (state, action) in path:
            self.N[(state, action)] += 1
            self.Q[(state, action)] += reward

    def select_action_ucb(self, state, available_actions):
        """
        Sélectionne une action en utilisant la formule Upper Confidence Bound (UCB).

        :param state: État actuel du jeu.
        :param available_actions: Actions disponibles dans l'état actuel.
        :return: Action choisie.
        """
        ucb_values = [(self.Q[(state, a)] / (1 + self.N[(state, a)]) +
                       self.exploration_weight * np.sqrt(np.log(sum(self.N[(state, a)] for a in available_actions) + 1e-10) / (1 + self.N[(state, a)])))
                      for a in available_actions]
        return available_actions[np.argmax(ucb_values)]

    def rollout_policy(self, state, available_actions):
        """
        Politique de déploiement: choisit une action en utilisant une heuristique.

        :param state: État actuel du jeu.
        :param available_actions: Actions disponibles dans l'état actuel.
        :return: Action choisie.
        """
        if random.random() < 0.1:  # 10% chance to choose a random action
            return random.choice(available_actions)
        
        max_gain = -1
        best_action = None
        for action in available_actions:
            gain = self.estimate_gain(state, action)
            if gain > max_gain:
                max_gain = gain
                best_action = action
        return best_action

    def estimate_gain(self, state, action):
        """
        Estime le gain d'une action en utilisant une heuristique.

        :param state: État actuel du jeu.
        :param action: Action à évaluer.
        :return: Gain estimé.
        """
        liste, joueur1 = list(state[:-1]), state[-1]
        trou_depart = action
        graines = liste[trou_depart]
        trou = trou_depart
        
        # Simulate sowing seeds
        while graines > 0:
            trou += 1
            if trou % 12 != trou_depart:
                graines -= 1
        
        # Calculate potential harvest
        prises = []
        while (liste[trou % 12] == 2 or liste[trou % 12] == 3) and ((joueur1 and trou % 12 > 5) or (not joueur1 and trou % 12 < 6)):
            prises.append(trou % 12)
            trou -= 1
        
        # Estimated gain is the sum of seeds in harvested holes
        estimated_gain = sum([liste[i] for i in prises])
        return estimated_gain

    def learn(self, *args, **kwargs):
        """
        Cette méthode est ajoutée pour assurer la compatibilité avec l'interface des agents.
        MCTS n'a pas besoin d'une étape d'apprentissage explicite car il construit l'arbre de recherche à chaque étape.
        """
        pass

    def load(self, filename):
        """
        Charge les poids de l'agent à partir d'un fichier.

        :param filename: Nom du fichier à charger.
        """
        with open(filename, 'rb') as f:
            self.Q, self.N = pickle.load(f)

    def save(self, filename):
        """
        Sauvegarde les poids de l'agent dans un fichier.

        :param filename: Nom du fichier dans lequel sauvegarder.
        """
        with open(filename, 'wb') as f:
            pickle.dump((self.Q, self.N), f)
