from tkinter import *
import numpy as np


class Partie(object):
    """Gère l'ensemble des opérations sur les grains"""
    def __init__(self):
        self.liste = [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4]
        self.joueur1 = True     # Est vrai si c'est au joueur 1 de jouer
        self.fin = False
        self.score = [0, 0]
        self.previous_states = set()
        
    
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
        """Renvoie l'état actuel du jeu."""
        return tuple(self.liste + [self.joueur1])

    def get_available_actions(self):
        """Renvoie les actions disponibles pour le joueur actuel."""
        return self.jouables

    def get_reward(self, captured_seeds):
        """Renvoie la récompense pour le joueur actuel."""
        return captured_seeds
    
    def coup(self, trou_depart):
        """Effectue les semailles et les récoltes"""
        current_state = self.get_state()
        if current_state in self.previous_states:
            self.fin = True  # Terminez la partie si l'état se répète
            return None
        self.previous_states.add(current_state)
        
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
        if self.score[0]>=25 or self.score[1]>=25 or (self.score[0]>=24 and self.score[1]>=24):
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