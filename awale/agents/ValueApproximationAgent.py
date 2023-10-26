from collections import defaultdict
import pickle

class ValueFunctionApproximation:
    def __init__(self, feature_extractor, learning_rate=0.1, discount_factor=0.9):
        self.feature_extractor = feature_extractor
        self.learning_rate = learning_rate
        self.weights = defaultdict(float)
        self.discount_factor = discount_factor  # Ajout de cette ligne


    def predict(self, state_action):
        features = self.feature_extractor(state_action)
        value = sum(self.weights[feature] * value for feature, value in features.items())
        return value

    def update_weights(self, state_action, target):
        features = self.feature_extractor(state_action)
        prediction = sum(self.weights[feature] * value for feature, value in features.items())
        error = target - prediction

        for feature, value in features.items():
            self.weights[feature] += self.learning_rate * error * value

    def choose_action(self, state, available_actions):
        best_action = None
        best_value = float('-inf')

        for action in available_actions:
            state_action = (state, action)
            value = self.predict(state_action)  # Modification ici
            if value > best_value:
                best_action = action
                best_value = value

        return best_action

    def learn(self, state, action, reward, next_state, next_actions):
        # Vérifiez si reward est None et définissez une valeur par défaut si nécessaire
        if reward is None:
            reward = 0.0  # ou toute autre valeur par défaut que vous jugez appropriée

        # Calculer la valeur cible
        next_values = [self.predict((next_state, next_action)) for next_action in next_actions]
        target_value = reward + self.discount_factor * max(next_values, default=0)

        # Mettre à jour les poids
        self.update_weights((state, action), target_value)
    

    def save_weights(self, file_path):
        with open(file_path, 'wb') as file:
            pickle.dump(self.weights, file)
            

    def load_weights(self, file_path):
        with open(file_path, 'rb') as file:
            loaded_weights = pickle.load(file)
            self.weights = loaded_weights
