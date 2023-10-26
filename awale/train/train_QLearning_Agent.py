from services.Partie import Partie

def train_QLearning_Agent(num_games, agent1, agent2):
    for num in range(num_games):
        print(num)
    
        
        partie = Partie()  # Initialisez une nouvelle partie
        while not partie.fin:
            state = partie.get_state()
            available_actions = partie.get_available_actions()

            if partie.joueur1:
                action = agent1.choose_action(state, available_actions)
            else:
                action = agent2.choose_action(state, available_actions)

            reward = partie.coup(action)
            next_state = partie.get_state()
            next_actions = partie.get_available_actions()

            if partie.joueur1:
                agent1.learn(state, action, reward, next_state, next_actions)
            else:
                agent2.learn(state, action, reward, next_state, next_actions)

        # # Sauvegardez les poids de l'agent après chaque partie (si nécessaire)
        # Sauvegardez les poids de l'agent après chaque partie (si nécessaire)
        if (num + 1) % 100 == 0:  # Sauvegardez les poids tous les 100 jeux par exemple
            agent1.save_weights(f"agent1_weights_game_{num + 1}.pkl")

            print(f"{(num//(num_games//100))}% achevé")
            print(f"{(num//(num_games//100)) * 5}% achevé")  # Multipliez par 5 pour obtenir le pourcentage correct

        # Charger les poids si un fichier de poids existe
        if num != 0 and (num + 1) % 100 == 0:  # suppose que les poids sont sauvegardés tous les 100 jeux
            agent1_file = f"agent1_weights_game_{num + 1}.pkl"
            agent1.load_weights(agent1_file)

        # Affiche le pourcentage de train achevé tout les 5%
        if num%(num_games//20)==0:
            print(f"{(num//(num_games//100))}% achevé")

        # À la fin de chaque partie, après la boucle while not partie.fin:
        vainqueur = partie.vainqueur  # 1 pour le joueur 1, 2 pour le joueur 2, 0 pour l'égalité
        score_joueur1, score_joueur2 = partie.score  # Obtient les scores des deux joueurs
        
        print(f'Win : {vainqueur}')
