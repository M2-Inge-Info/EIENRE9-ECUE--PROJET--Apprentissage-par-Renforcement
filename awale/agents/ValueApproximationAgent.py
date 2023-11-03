# ValueFunctionApproximation.py
"""
ValueFunctionApproximation: Un agent qui choisit une approximation de la fonction de valeur à l'aide de l'apprentissage par renforcement.

Auteur: GR Awalé
"""

from collections import defaultdict, deque
import numpy as np
import pickle

class ValueFunctionApproximation:
    """
    Classe représentant une approximation de la fonction de valeur à l'aide de l'apprentissage par renforcement.

    Attributs:
        feature_extractor (callable): Fonction pour extraire les caractéristiques d'une paire état-action.
        learning_rate (float): Taux d'apprentissage pour la mise à jour des poids.
        weights (dict): Poids associés aux caractéristiques.
        discount_factor (float): Facteur d'actualisation des récompenses futures.
        epsilon (float): Probabilité d'exploration dans la stratégie epsilon-greedy.
        decay_factor (float): Facteur de décroissance pour epsilon et learning_rate.
        regularization_factor (float): Facteur de régularisation pour la mise à jour des poids.
        memory (deque): Mémoire pour stocker les expériences passées.

    Méthodes:
        - predict: Prédit la valeur de la paire état-action.
        - update_weights: Met à jour les poids en fonction de l'erreur entre la prédiction et la cible.
        - choose_action: Sélectionne une action selon une stratégie epsilon-greedy.
        - learn: Met à jour les poids en fonction de l'expérience (état, action, récompense, état suivant).
        - save_weights: Sauvegarde les poids actuels dans un fichier.
        - load_weights: Charge les poids à partir d'un fichier.
    """

    def __init__(self, feature_extractor, learning_rate=0.1, discount_factor=0.9, epsilon=0.1, decay_factor=0.995, regularization_factor=0.01, memory_size=1000):
        self.feature_extractor = feature_extractor
        self.learning_rate = learning_rate
        self.weights = defaultdict(float)
        self.discount_factor = discount_factor
        self.epsilon = epsilon
        self.decay_factor = decay_factor
        self.regularization_factor = regularization_factor
        self.memory = deque(maxlen=memory_size)

    def predict(self, state_action):
        """
        Prédit la valeur de la paire état-action en utilisant les caractéristiques et les poids actuels.

        :param state_action: Tuple (état, action).
        :return: Valeur prédite.
        """
        features = self.feature_extractor(state_action)
        value = sum(self.weights[feature] * value for feature, value in features.items())
        return value

    def update_weights(self, state_action, target):
        """
        Met à jour les poids en fonction de l'erreur entre la prédiction et la cible.

        :param state_action: Tuple (état, action).
        :param target: Valeur cible à atteindre.
        """
        features = self.feature_extractor(state_action)
        prediction = sum(self.weights[feature] * value for feature, value in features.items())
        error = target - prediction

        for feature, value in features.items():
            self.weights[feature] += self.learning_rate * (error * value - self.regularization_factor * self.weights[feature])

    def choose_action(self, state, available_actions):
        """
        Sélectionne une action selon une stratégie epsilon-greedy.

        :param state: État actuel du jeu.
        :param available_actions: Liste des actions disponibles.
        :return: Action choisie.
        """
        if np.random.uniform(0, 1) < self.epsilon:
            return np.random.choice(available_actions)
        else:
            best_action = max(available_actions, key=lambda action: self.predict((state, action)))
            return best_action

    def learn(self, state, action, reward, next_state, next_actions):
        """
        Met à jour les poids en fonction de l'expérience (état, action, récompense, état suivant).

        :param state: État actuel.
        :param action: Action effectuée.
        :param reward: Récompense reçue.
        :param next_state: État suivant.
        :param next_actions: Actions disponibles dans l'état suivant.
        """
        reward = reward if reward is not None else 0.0
        target_value = reward + self.discount_factor * max((self.predict((next_state, next_action)) for next_action in next_actions), default=0)
        self.update_weights((state, action), target_value)
        self.learning_rate *= self.decay_factor
        self.epsilon *= self.decay_factor


    def save_weights(self, file_path):
        """
        Sauvegarde les poids actuels dans un fichier.

        :param file_path: Chemin du fichier où sauvegarder les poids.
        """
        with open(file_path, 'wb') as file:
            pickle.dump(self.weights, file)

    def load_weights(self, file_path):
        """
        Charge les poids à partir d'un fichier.

        :param file_path: Chemin du fichier à partir duquel charger les poids.
        """
        with open(file_path, 'rb') as file:
            loaded_weights = pickle.load(file)
            self.weights = loaded_weights
