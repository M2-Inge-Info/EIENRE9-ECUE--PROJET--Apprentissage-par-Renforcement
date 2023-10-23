from collections import defaultdict

class ValueFunctionApproximation:
    def __init__(self, feature_extractor, learning_rate=0.1):
        self.feature_extractor = feature_extractor  # Assurez-vous que feature_extractor est une fonction
        self.learning_rate = learning_rate
        self.weights = defaultdict(float)

    def predict(self, state):
        features = self.extract_features(state)
        value = sum(self.weights[feature] * value for feature, value in features.items())
        return value

    def update_weights(self, state, target):
        features = self.feature_extractor(state)
        prediction = sum(self.weights[feature] * value for feature, value in features.items())
        error = target - prediction

        for feature, value in features.items():
            self.weights[feature] += self.learning_rate * error * value

    def choose_action(self, state, available_actions):
        # Choose the action with the highest estimated value
        best_action = None
        best_value = float('-inf')

        for action in available_actions:
            state_action = (state, action)
            value = self.predict(state_action)
            if value > best_value:
                best_action = action
                best_value = value

        return best_action

    def extract_features(self, state):
        """
        Extracts features from the game state.
        Args:
            state: A tuple representing the game state. For example, (board, score_player1, score_player2, current_player).
        Returns:
            A dictionary of features.
        """
        board, score_player1, score_player2, current_player = state

        features = {}

        for i, seeds in enumerate(board):
            features[f'board_{i}'] = seeds

        features['score_player1'] = score_player1
        features['score_player2'] = score_player2

        features['current_player'] = current_player

        capture_possible = 0
        for i in range(6):
            if current_player == 1 and 0 < board[i] <= 6 - i:
                capture_possible = 1
            elif current_player == 2 and 0 < board[i + 6] <= 12 - i:
                capture_possible = 1

        features['capture_possible'] = capture_possible

        return features
