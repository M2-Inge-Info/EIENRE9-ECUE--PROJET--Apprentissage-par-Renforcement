from services.Partie import Partie
import numpy as np

def train_DQN_Agents(num_games, agent1, agent2):
    for game in range(num_games):
        # Créer une nouvelle instance de jeu à chaque itération
        game_instance = Partie()  # Remplacez ceci par la façon dont vous initialisez une nouvelle partie dans votre jeu

        while not game_instance.fin:
            # Obtenir l'état actuel et les actions disponibles
            state = np.array(game_instance.get_state())
            available_actions = game_instance.get_available_actions()

            if game_instance.joueur1:
                action = agent1.act(state.reshape(1, -1))
            else:
                action = agent2.act(state.reshape(1, -1))

            # Jouer l'action et obtenir la récompense
            reward = game_instance.coup(action)
            print(reward)
            next_state = np.array(game_instance.get_state())

            # Mémoriser l'expérience
            done = game_instance.fin
            if game_instance.joueur1:
                agent1.remember(state, action, reward, next_state, done)
            else:
                agent2.remember(state, action, reward, next_state, done)

            # Faire l'expérience du replay pour apprendre
            agent1.replay()
            agent2.replay()

        # Vous pouvez ajouter des logs ici pour suivre la progression, par exemple :
        if (game + 1) % 100 == 0:
            print(f'Game {game + 1}/{num_games} finished.')

    # Sauvegardez les poids des agents après l'entraînement
    agent1.save('agent1_weights.h5')
    agent2.save('agent2_weights.h5')
