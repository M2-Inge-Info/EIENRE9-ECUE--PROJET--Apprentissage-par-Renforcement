#!/usr/bin/env python3

from tkinter import *

import numpy as np

from agents.QLearningAgent import QLearningAgent
from agents.RandomAgent import RandomAgent
from agents.ValueApproximationAgent import ValueFunctionApproximation

from train.train_QLearning_Agent import train_QLearning_Agent

from services.Partie import Partie

class Application(Tk):
    """Classe gérant l'interface graphique pour le jeu d'awalé"""
    def __init__(self):
        Tk.__init__(self)
        self.title("Jeu d'awalé")
        self.resizable(0,0)
        barre_menu = Menu(self)        # Menus
        menu_jeu = Menu(barre_menu, tearoff=0)
        barre_menu.add_cascade(label="Jeu", menu=menu_jeu)
        menu_jeu.add_command(label="(Re)commencer une partie", command=self.debut_jeu)
        menu_jeu.add_separator()
        menu_jeu.add_command(label="Quitter", command=self.destroy)
        self.config(menu=barre_menu)
        self.canvas = Canvas(self, width=555, height=350)   # Grand canvas et plateau
        self.canvas.create_rectangle(0, 70, 555, 280, fill='black')
        liste_lettres1 = ["a","b","c","d","e","f"]
        liste_lettres2 = ["A","B","C","D","E","F"]
        for i in range(6):
            self.canvas.create_oval(i*90+15, 85, i*90+90, 160, fill='brown')
            self.canvas.create_text(i*90+15, 85, text=liste_lettres1[i], font=('serif', 13), fill='green')
            self.canvas.create_oval(i*90+15, 190, i*90+90, 265, fill='brown')
            self.canvas.create_text(i*90+15, 190, text=liste_lettres2[i], font=('serif', 11), fill='green')
        self.canvas.create_line(10, 175, 540, 175, fill='brown')
        self.canvas.pack(side=LEFT, padx=3, pady=3)
        self.id_joueur = None       # Identifiants (pour pouvoir supprimer)
        self.id_correctif = None
        self.ids_nombres = []
        self.ids_joueurs = []
        self.id_couronne = None
        self.canvas.bind('<Button-1>', self.detection_coup)
        self.debut_jeu()
        # self.choose_adversaries()

        # self.agent1 = ValueFunctionApproximation(self.extract_features, learning_rate=0.1, discount_factor=0.9)
        # self.agent2 = RandomAgent()

        # self.train_agent(1000)

        self.agent1 = QLearningAgent()

        self.agent2 = RandomAgent()
        agent1_file = f"agent1_weights_game_7500.pkl"
        self.agent1.load_weights(agent1_file)
        self.play_with_agents()
            

    def choose_adversaries(self):
        # Créez une nouvelle fenêtre pour la sélection des adversaires
        self.choice_window = Toplevel(self)
        self.choice_window.title("Choisir les adversaires")

        # Ajoutez des boutons radio ou une liste déroulante pour sélectionner les adversaires
        # Pour cet exemple, je vais utiliser des boutons radio
        self.agent1_choice = StringVar(value="ValueFunctionApproximation")
        self.agent2_choice = StringVar(value="QLearningAgent")

        Label(self.choice_window, text="Choisir l'adversaire pour le joueur 1:").pack(pady=10)
        Radiobutton(self.choice_window, text="ValueFunctionApproximation", variable=self.agent1_choice, value="ValueFunctionApproximation").pack(anchor=W)
        Radiobutton(self.choice_window, text="RandomAgent", variable=self.agent1_choice, value="RandomAgent").pack(anchor=W)

        Label(self.choice_window, text="Choisir l'adversaire pour le joueur 2:").pack(pady=10)
        Radiobutton(self.choice_window, text="QLearningAgent", variable=self.agent2_choice, value="QLearningAgent").pack(anchor=W)
        Radiobutton(self.choice_window, text="RandomAgent", variable=self.agent2_choice, value="RandomAgent").pack(anchor=W)

        Button(self.choice_window, text="Commencer", command=self.start_game).pack(pady=20)

    def start_game(self):
        # Ici, vous pouvez initialiser vos agents en fonction des choix
        if self.agent1_choice.get() == "ValueFunctionApproximation":
            self.agent1 = ValueFunctionApproximation(self.extract_features, learning_rate=0.1, discount_factor=0.9)
        elif self.agent1_choice.get() == "RandomAgent":
            self.agent1 = RandomAgent()

        if self.agent2_choice.get() == "QLearningAgent":
            self.agent2 = QLearningAgent()
        elif self.agent2_choice.get() == "RandomAgent":
            self.agent2 = RandomAgent()

        # Fermez la fenêtre de choix
        self.choice_window.destroy()

        self.agent1 = QLearningAgent()

        print(self.agent1)
        print(self.agent2)
        
        agent1_file = f"agent1_weights_game_7500.pkl"
        self.agent1.load_weights(agent1_file)

        # Commencez le jeu
        self.debut_jeu()
        self.play_with_agents()

    def end_game(self):
        # À la fin du jeu, affichez un bouton "Quitter"
        Button(self, text="Quitter", command=self.quit_game).pack(pady=20)

    def quit_game(self):
        # Fermez l'application
        self.destroy()

    def extract_features(self, state_action):
        state, action = state_action
        features = {}
        for i, s in enumerate(state):
            features[f"state_{i}"] = s
        features["action"] = action
        return features

    def debut_jeu(self):        # Au début d'une partie
        self.p = Partie()
        if self.id_couronne:
            self.canvas.delete(self.id_couronne)
        self.ecrire_nombres(self.p.liste)
        self.ecrire_scores((self.p.score[0], self.p.score[1]))
        self.affiche_joueur()
    
    def detection_coup(self, event):
        # def lettre(x, y):
        #     if 85<y<160 and (15<x<540 and 0<(x-15)%90<75):
        #         return ["a","b","c","d","e","f"][(x-15)//90]
        #     elif 190<y<265 and 15<x<540:
        #         return ["A","B","C","D","E","F"][(x-15)//90]
        #     else:
        #         return ""
        # self.jouer(lettre(event.x, event.y))
        pass

    def jouer(self, trou):        # Fonction principale
        try:
            t = {"A":0,"B":1,"C":2,"D":3,"E":4,"F":5,"f":6,"e":7,"d":8,"c":9,"b":10,"a":11}[trou]
        except:
            return None
        if not t in self.p.jouables:
            return None
        else:
            self.p.coup(t)
            self.ecrire_scores((self.p.score[0], self.p.score[1]))
            self.ecrire_nombres(self.p.liste)
            self.affiche_joueur()
            if self.p.vainqueur:
                self.couronne()

        if not self.p.fin:
            self.after(200, self.play_with_agents)
        self.update_ui()


    def play_with_agents(self):
        if not self.p.fin:
            state = self.p.get_state()
            available_actions = self.p.get_available_actions()

            if self.p.joueur1:
                action = self.agent1.choose_action(state, available_actions)
            else:
                # Utilisez l'agent aléatoire pour le joueur 2
                action = self.agent2.choose_action(state, available_actions)
            
            reward = self.p.coup(action)
            next_state = self.p.get_state()
            next_actions = self.p.get_available_actions()
            
            if self.p.joueur1:
                self.agent1.learn(state, action, reward, next_state, next_actions)
            else:
                self.agent2.learn(state, action, reward, next_state, next_actions)
            
            self.update_ui()
            self.after(100, self.play_with_agents)  # Continuez à jouer après 1 seconde

    
    def ecrire_nombres(self, liste):    # Écrit les graines
        for i in self.ids_nombres:
            self.canvas.delete(i)
        self.ids_nombres = []
        for i in range(6):
            self.ids_nombres.append(self.canvas.create_text(i*90+50, 225, text=str(liste[i]), fill='blue', font=('Arial',28,'bold')))
        for i in range(6):
            self.ids_nombres.append(self.canvas.create_text(555-(i*90+50), 120, text=str(liste[6+i]), fill='blue', font=('Arial',28,'bold')))
    
    def ecrire_scores(self, scores):    # Écrit les joueurs et leurs scores
        for i in self.ids_joueurs:
            self.canvas.delete(i)
        self.ids_joueurs = []
        self.ids_joueurs.append(self.canvas.create_text(555/2, 315, text="Joueur n°1 (%s)" %(str(scores[0])+(" pts." if scores[0]>=2 else " pt.")), font=('Helvetica', 20)))
        self.ids_joueurs.append(self.canvas.create_text(555/2, 35, text="Joueur n°2 (%s)" %(str(scores[1])+(" pts." if scores[1]>=2 else " pt.")), font=('Helvetica', 20)))
    
    def affiche_joueur(self):           # Affiche le joueur dont c'est le tour
        self.title("Jeu d'awale - " + ("Joueur 1" if self.p.joueur1 else "Joueur 2"))
        
    def couronne(self):                     # Affiche une couronne à coté du vainqueur
        x = 110
        y = 325 if self.p.vainqueur==1 else 45 
        self.id_couronne = self.canvas.create_polygon(x, y, x, y-25, x+6, y-7, x+12, y-25, x+18, y-7, x+24, y-25, x+30, y-7, x+36, y-25, x+36, y, fill='gold')

    def update_ui(self):
        # Mettre à jour l'interface graphique après chaque action
        self.ecrire_scores((self.p.score[0], self.p.score[1]))
        self.ecrire_nombres(self.p.liste)
        self.affiche_joueur()
        if self.p.vainqueur:
            self.couronne()

if __name__ == '__main__':
    Application().mainloop()

# if __name__ == '__main__':
#     q_learning_agent = QLearningAgent()
#     random_agent = RandomAgent()
#     train_QLearning_Agent(10000, q_learning_agent, random_agent)
