# from services.Partie import Partie

# def calculate_reward(partie, old_state, new_state):
#     old_score_joueur1, old_score_joueur2 = partie.score  # Assume partie.score returns the current scores
#     new_score_joueur1, new_score_joueur2 = new_state[-2:]  # Assume the scores are the last two elements in the state tuple

#     # Calculate the difference in scores
#     diff_score_joueur1 = new_score_joueur1 - old_score_joueur1
#     diff_score_joueur2 = new_score_joueur2 - old_score_joueur2

#     # Adjust the reward based on the difference in scores
#     reward = diff_score_joueur1 - diff_score_joueur2

#     # Additional rewards or penalties based on win, loss, or tie
#     if partie.fin:
#         if partie.vainqueur == 1:
#             reward = 1.2  # Reward for winning
#         elif partie.vainqueur == 2:
#             reward = -1  # Penalty for losing
#         else:
#             reward = -0.2  # Lesser reward for a tie

#     return reward



# def train_QLearning_Agent(num_games, agent1, agent2, process_id):
#     scores_joueur1 = []  # List to hold scores for joueur1
#     scores_joueur2 = []  # List to hold scores for joueur2
    
#     for num in range(num_games):
#         print(num)
    
#         partie = Partie()  # Initialisez une nouvelle partie
#         while not partie.fin:
#             old_state = partie.get_state()  # Enregistrez l'état actuel avant de prendre une action
#             available_actions = partie.get_available_actions()

#             if partie.joueur1:
#                 action = agent1.choose_action(old_state, available_actions)
#             else:
#                 action = agent2.choose_action(old_state, available_actions)

#             partie.coup(action)  # Jouez le coup, mais la récompense sera calculée différemment
#         new_state = partie.get_state()  # Obtenez le nouvel état après avoir pris l'action

#         # Calculer la récompense basée sur l'ancien et le nouvel état
#         reward =calculate_reward(partie, old_state, new_state)
#         # print(f"Reward: {reward}")  # Ajoutez cette ligne

#         next_actions = partie.get_available_actions()

#         if partie.joueur1:
#             agent1.learn(old_state, action, reward, new_state, next_actions)
#         else:
#             agent2.learn(old_state, action, reward, new_state, next_actions)

#         # print(f"End of game {num + 1}. Winner: {partie.vainqueur}")

#         # # Sauvegardez les poids de l'agent après chaque partie (si nécessaire)
#         # Sauvegardez les poids de l'agent après chaque partie (si nécessaire)
#         if (num + 1) % 5000 == 0:  # Sauvegardez les poids tous les 100 jeux par exemple
#             file_name = f"agent1_weights_game_{num + 1}_process_{process_id}.pkl"
#             agent1.save_weights(file_name)

#             # print(f"{(num//(num_games//100))}% achevé")
#             # print(f"{(num//(num_games//100)) * 5}% achevé")  # Multipliez par 5 pour obtenir le pourcentage correct
            
#             # agent1.load_weights(file_name)


#         # Affiche le pourcentage de train achevé tout les 5%
#         if num%(num_games//20)==0:
#             print(f"{(num//(num_games//100))}% achevé")

#         vainqueur = partie.vainqueur  # 1 for joueur 1, 2 for joueur 2, 0 for a tie
#         score_joueur1, score_joueur2 = partie.score  # Get the scores for both players

#         scores_joueur1.append(score_joueur1)
#         scores_joueur2.append(score_joueur2)
        
#         print(f'Win : {vainqueur}')
#     return scores_joueur1, scores_joueur2  # Return the scores at the end of training


# def evaluate_agent(agent, num_episodes):
#     total_rewards = 0
#     for _ in range(num_episodes):
#         partie = Partie()  # Initialisez une nouvelle partie
#         while not partie.fin:
#             state = partie.get_state()
#             available_actions = partie.get_available_actions()
#             action = agent.choose_action(state, available_actions, exploit=True)
#             partie.coup(action)  # Jouez le coup
#             reward = calculate_reward(partie, state, partie.get_state())
#             total_rewards += reward
#     average_reward = total_rewards / num_episodes
#     print(f"Average reward over {num_episodes} episodes: {average_reward}")
    
    
    
    


# from collections import defaultdict, deque
# import numpy as np
# import random
# import pickle

# class QLearningAgent:
#     def __init__(self, alpha=0.2, gamma=0.9, epsilon=1.0, epsilon_decay=0.995, epsilon_min=0.01, batch_size=128, memory_size=10000, alpha_decay=0.995):
#         self.alpha = alpha
#         self.gamma = gamma
#         self.epsilon = epsilon
#         self.epsilon_decay = epsilon_decay
#         self.epsilon_min = epsilon_min
#         self.Q1 = defaultdict(float)
#         self.Q2 = defaultdict(float)
#         self.memory = deque(maxlen=memory_size)
#         self.batch_size = batch_size
#         self.alpha_decay = alpha_decay
#         self.priority_beta = 0.4
#         self.priority_epsilon = 1e-6
#         self.priorities = defaultdict(lambda: 1.0)  # Initialisation des priorités à 1.0

#     def choose_action(self, state, available_actions, exploit=False):
#         # if not exploit and np.random.uniform(0, 1) < self.epsilon:
#         #     print("au pif encore")
#         #     return np.random.choice(available_actions)
#         avg_Q = lambda action: (self.Q1[(state, action)] + self.Q2[(state, action)]) / 2
#         return max(available_actions, key=avg_Q)

#     def learn(self, state, action, reward, next_state, next_actions):
#         self.memory.append((state, action, reward, next_state, next_actions))
        
#         if len(self.memory) < self.batch_size:
#             print("size return")
#             return

#         probabilities = np.array([self.priorities[(state, action)] for state, action, _, _, _ in self.memory])
#         total_prob = np.sum(probabilities)

#         if total_prob == 0 or np.isnan(total_prob):
#             probabilities = np.ones_like(probabilities) / len(self.memory)
#         else:
#             probabilities /= total_prob

#         if np.any(np.isnan(probabilities)):
#             # print("Warning: NaN values detected in probabilities!")
#             probabilities = np.ones_like(probabilities) / len(self.memory)

#         batch_indices = np.random.choice(len(self.memory), self.batch_size, p=probabilities)
#         batch = [self.memory[i] for i in batch_indices]
#         # Dans la méthode learn de votre agent
#         # print(f"Q1 before update: {self.Q1[(state, action)]}")
#         # print(f"Q2 before update: {self.Q2[(state, action)]}")


#         for idx, (state, action, reward, next_state, next_actions) in enumerate(batch):
#             if len(next_actions) == 0:  # Changez la condition ici
#                 print("next actions condition triggered")
#                 continue
#             else:
#                 # Dans la méthode learn de votre agent
#                 if np.random.rand() < 0.5:
#                     next_max_action = max(next_actions, key=lambda a: self.Q1[(next_state, a)])
#                     target_Q = reward + self.gamma * self.Q2[(next_state, next_max_action)]
#                     td_error = target_Q - self.Q1[(state, action)]
#                     # print(f"TD Error: {td_error}")  # Ajoutez cette ligne
#                     self.Q1[(state, action)] += self.alpha * td_error
#                 else:
#                     next_max_action = max(next_actions, key=lambda a: self.Q2[(next_state, a)])
#                     target_Q = reward + self.gamma * self.Q1[(next_state, next_max_action)]
#                     td_error = target_Q - self.Q2[(state, action)]
#                     # print(f"TD Error: {td_error}")  # Ajoutez cette ligne
#                     self.Q2[(state, action)] += self.alpha * td_error

#                 # print(f"Q1 after update: {self.Q1[(state, action)]}")  # Ajoutez cette ligne
#                 # print(f"Q2 after update: {self.Q2[(state, action)]}") 

#             td_error = target_Q - self.Q1[(state, action)]
#             self.Q1[(state, action)] += self.alpha * td_error
#             self.priorities[(state, action)] = abs(td_error) + self.priority_epsilon

#         if self.epsilon > self.epsilon_min:
#             self.epsilon *= self.epsilon_decay

#         self.alpha *= self.alpha_decay
#         # print("ok learn ")

#     def save_weights(self, file_path):
#         with open(file_path, 'wb') as file:
#             pickle.dump((self.Q1, self.Q2), file)

#     def load_weights(self, file_path):
#         with open(file_path, 'rb') as file:
#             self.Q1, self.Q2 = pickle.load(file)

