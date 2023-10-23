#!/usr/bin/env python3

from tkinter import *

import numpy as np

from QLearningAgent import QLearningAgent
from ValueApproximationAgent import ValueFunctionApproximation
from agents.RandomAgent import RandomAgent

class Partie(object):
    """Gère l'ensemble des opérations sur les grains"""
    def __init__(self):
        self.liste = [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4]
        self.joueur1 = True     # Est vrai si c'est au joueur 1 de jouer
        self.fin = False
        self.score = [0, 0]
    
    @property
    def jouables(self):
        """Renvoie la liste des trous jouables"""
        j = tuple(i for i in list(range(0,6) if self.joueur1 else range(6,12)) if self.liste[i]!=0) # Les trous doivent être du bon coté et contenir quelque chose
        if self.joueur1 and sum(self.liste[6:])==0:         # Le joueur 1 peut être contraint de jouer certaines cases pour nourrir le joueur 2 
            return tuple(i for i in j if self.liste[i]>5-i)
        elif not self.joueur1 and sum(self.liste[:6])==0:
            return tuple(i for i in j if self.liste[i]>11-i)
        else:
            return j
    
    @property
    def vainqueur(self):
        """Renvoie le vainqueur"""
        if not self.fin:
            return None
        else:
            if self.score[0]>self.score[1]:
                return 1
            elif self.score[0]<self.score[1]:
                return 2
            else:
                return 0
    
    def get_state(self):
        """Renvoie l'état actuel du jeu sous forme de quatre caractéristiques."""
        board = self.liste
        score_player1 = self.score[0]
        score_player2 = self.score[1]
        current_player = 1 if self.joueur1 else 2  # Assignez 1 au joueur 1 et 2 au joueur 2
        return board, score_player1, score_player2, current_player


    def get_available_actions(self):
        """Renvoie les actions disponibles pour le joueur actuel."""
        return self.jouables

    def get_reward(self, captured_seeds):
        """Renvoie la récompense pour le joueur actuel."""
        return captured_seeds
    
    def coup(self, trou_depart):
        """Effectue les semailles et les récoltes"""
        if trou_depart not in self.jouables:
            return None
        graines = self.liste[trou_depart]   # Récupère le nombre de graines à semer
        self.liste[trou_depart] = 0
        trou = trou_depart
        while graines>0:                    # Sème les graines
            trou+=1
            if trou%12!=trou_depart:
                self.liste[trou%12] += 1
                graines-=1
        prises = []
        while (self.liste[trou%12]==2 or self.liste[trou%12]==3) and ((self.joueur1 and trou%12>5) or (not self.joueur1 and trou%12<6)):    # Calcule les prises en partant du dernier trou
            prises.append(trou%12)
            trou-=1
        self.gain = sum([self.liste[i] for i in prises])
        if ((self.joueur1 and len([i for i in self.liste[6:] if i==0])+len(prises)==6) or (not self.joueur1 and len([i for i in self.liste[:6] if i==0])+len(prises)==6)) or len(prises)==0:  # On ne prend pas si cela affame
            pass
        else:
            for i in prises:
                self.liste[i] = 0  # Les trous sont vidés...
            if self.joueur1:
                self.score[0] += self.gain  # ...et les graines récoltés
            else:
                self.score[1] += self.gain
        self.joueur1 = not self.joueur1 # Changement de joueur
        if self.jouables==():       # Fin (car le joueur ne peut plus nourrir son adversaire)
            if self.joueur1:
                self.score[0]+= sum(self.liste)
            else:
                self.score[1]+= sum(self.liste)
            self.liste = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
            self.fin = True
        # Si le score d'un des joueurs atteint 25, la partie est terminée
        if self.score[0]>=25 or self.score[1]>=25:
            self.fin = True

        return self.gain
    
    def jouer(self):
        """Permet de jouer en mode non-graphique"""
        print(" "*10+"Jeu d'awalé")
        print("\n"+str([self.liste[i] for i in range(11, 5,-1)])+"\n"+str(self.liste[:6]))
        while not self.fin:     # Boucle principale
            print("\n--Joueur n°1 (%s pts)--" %self.score[0] if self.joueur1 else "\n--Joueur n°2 (%s pts)--" %self.score[1])
            while True:
                try:
                    t = int(input("Choisissez un nombre %s : " %str(self.jouables)))
                except:
                    print("Vous n'avez pas saisi un nombre.")
                    continue
                if t in self.jouables:
                    break
                else:
                    print("Vous ne pouvez pas jouer cela.")
                    continue
            self.coup(t)
            print(str([self.liste[i] for i in range(11, 5,-1)])+"\n"+str(self.liste[:6]))
            if self.gain!=0:
                print("+1 point" if self.gain==1 else "+ %s points" %str(self.gain))
        print("Partie terminée.")
        if self.vainqueur != 0:
            print("Le joueur n° %s a gagné." %str(self.vainqueur))
        else:
            print("Egalité.")

class Application(Tk):
    def __init__(self):
        Tk.__init__(self)
        self.title("Jeu d'awalé")
        self.resizable(0, 0)
        barre_menu = Menu(self)  # Menus
        menu_jeu = Menu(barre_menu, tearoff=0)
        barre_menu.add_cascade(label="Jeu", menu=menu_jeu)
        menu_jeu.add_command(label="(Re)commencer une partie", command=self.debut_jeu)
        menu_jeu.add_separator()
        menu_jeu.add_command(label="Quitter", command=self.destroy)
        self.config(menu=barre_menu)
        self.canvas = Canvas(self, width=555, height=350)  # Grand canvas et plateau
        self.canvas.create_rectangle(0, 70, 555, 280, fill='black')
        liste_lettres1 = ["a", "b", "c", "d", "e", "f"]
        liste_lettres2 = ["A", "B", "C", "D", "E", "F"]
        for i in range(6):
            self.canvas.create_oval(i * 90 + 15, 85, i * 90 + 90, 160, fill='brown')
            self.canvas.create_text(i * 90 + 15, 85, text=liste_lettres1[i], font=('serif', 13), fill='green')
            self.canvas.create_oval(i * 90 + 15, 190, i * 90 + 90, 265, fill='brown')
            self.canvas.create_text(i * 90 + 15, 190, text=liste_lettres2[i], font=('serif', 11), fill='green')
        self.canvas.create_line(10, 175, 540, 175, fill='brown')
        self.canvas.pack(side=LEFT, padx=3, pady=3)

        self.id_couronne = None
        self.ids_nombres = []  # Initialisez ids_nombres à une liste vide
        self.ids_joueurs = []  # Initialisez ids_joueurs à une liste vide

        self.debut_jeu()  # Déplacez cette ligne ici

        # Assurez-vous que self.p est maintenant défini
        self.extract_features = self.p.get_state
        self.agent1 = QLearningAgent()
        self.agent2 = ValueFunctionApproximation(self.extract_features)


        
    def debut_jeu(self):
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
                action = self.agent2.choose_action(state, available_actions)

            reward = self.p.coup(action)
            next_state = self.p.get_state()
            next_actions = self.p.get_available_actions()

            if self.p.joueur1:
                self.agent1.learn(state, action, reward, next_state, next_actions)
            # Pas besoin d'apprendre pour l'agent aléatoire

            # Mettez à jour la Value Function Approximation après chaque coup
            learning_rate = 0.1  # Taux d'apprentissage
            target = reward + self.agent2.predict(next_state)
            self.agent2.update_weights(state, target)

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
