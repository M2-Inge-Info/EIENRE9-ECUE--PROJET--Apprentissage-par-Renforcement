#!/usr/bin/env python3

from tkinter import *
from agents.QLearningAgent import QLearningAgent
from agents.RandomAgent import RandomAgent
from agents.ValueApproximationAgent import ValueFunctionApproximation
from agents.HumanAgent import HumanAgent
from agents.MCTSAgent import MCTSAgent
from services.Partie import Partie

class Application(Tk):
    """Classe gérant l'interface graphique pour le jeu d'awalé"""
    def __init__(self):
        super().__init__()
        self.ids_nombres = []  # Ajoutez cette ligne pour initialiser ids_nombres
        self.ids_joueurs = []  
        self.title("Jeu d'awalé")
        self.resizable(0, 0)
        self.setup_menu()
        self.setup_canvas()
        self.setup_agent_choices()
        self.debut_jeu()

    def setup_menu(self):
        barre_menu = Menu(self)
        menu_jeu = Menu(barre_menu, tearoff=0)
        barre_menu.add_cascade(label="Jeu", menu=menu_jeu)
        menu_jeu.add_command(label="(Re)commencer une partie", command=self.debut_jeu)
        menu_jeu.add_separator()
        menu_jeu.add_command(label="Quitter", command=self.destroy)
        self.config(menu=barre_menu)

    def setup_canvas(self):
        self.canvas = Canvas(self, width=555, height=350)
        self.canvas.create_rectangle(0, 70, 555, 280, fill='black')
        liste_lettres1, liste_lettres2 = ["a", "b", "c", "d", "e", "f"], ["A", "B", "C", "D", "E", "F"]
        for i in range(6):
            self.canvas.create_oval(i * 90 + 15, 85, i * 90 + 90, 160, fill='brown')
            self.canvas.create_text(i * 90 + 15, 85, text=liste_lettres1[i], font=('serif', 13), fill='green')
            self.canvas.create_oval(i * 90 + 15, 190, i * 90 + 90, 265, fill='brown')
            self.canvas.create_text(i * 90 + 15, 190, text=liste_lettres2[i], font=('serif', 11), fill='green')
        self.agent_info_label = Label(self, text="Agent 1 vs Agent 2", font=('Helvetica', 16))
        self.agent_info_label.pack(pady=10)
        self.canvas.create_line(10, 175, 540, 175, fill='brown')
        self.canvas.pack(side=LEFT, padx=3, pady=3)
        self.canvas.bind('<Button-1>', self.detection_coup)

    def setup_agent_choices(self):
        self.agent1_choice, self.agent2_choice = StringVar(value="Human"), StringVar(value="Human")
        self.create_agent_choice_widgets("Choisir l'adversaire pour le joueur 1:", self.agent1_choice)
        self.create_agent_choice_widgets("Choisir l'adversaire pour le joueur 2:", self.agent2_choice)
        Button(self, text="Commencer", command=self.start_game, fg="white", bg="green", activebackground="darkgreen", activeforeground="white").pack(pady=20)

    def create_agent_choice_widgets(self, label_text, agent_choice_var):
        agent_colors = {
            "Human": ("blue", "lightblue"),
            "QLearning": ("green", "lightgreen"),
            "VFA": ("red", "#FF8080"),
            "MCTS": ("purple", "plum"),
            "Random": ("orange", "lightyellow")  # Ajoutez cette ligne pour inclure le RandomAgent
        }
        Label(self, text=label_text).pack(pady=10)
        for agent_type, (fg_color, bg_color) in agent_colors.items():
            Radiobutton(self, text=agent_type, variable=agent_choice_var, value=agent_type, foreground=fg_color, selectcolor=bg_color).pack(anchor=W)


    def replay_game(self):
        """Redémarre le jeu."""
        self.debut_jeu()
        # self.start_game()

    def extract_features(self, state_action):
        state, action = state_action
        features = {}
        for i, s in enumerate(state):
            features[f"state_{i}"] = s
        features["action"] = action
        return features

    def start_game(self):
        agent_mapping = {
            "Human": HumanAgent,
            "QLearning": QLearningAgent,
            "VFA": lambda: ValueFunctionApproximation(feature_extractor=self.extract_features),
            "MCTS": MCTSAgent,
            "Random": RandomAgent  # Ajoutez cette ligne pour inclure le RandomAgent
        }
        self.agent1 = agent_mapping[self.agent1_choice.get()]()
        self.agent2 = agent_mapping[self.agent2_choice.get()]()
        self.agent_info_label.config(text=f"Agent 1: {self.agent1_choice.get()} vs Agent 2: {self.agent2_choice.get()}")
        self.play_with_agents()


    def debut_jeu(self):
        self.p = Partie()
        self.canvas.delete(self.id_couronne) if hasattr(self, 'id_couronne') else None
        self.replay_button.destroy() if hasattr(self, 'replay_button') else None
        self.ecrire_nombres(self.p.liste)
        self.ecrire_scores((self.p.score[0], self.p.score[1]))
        self.affiche_joueur()
    
    def detection_coup(self, event):
        def lettre(x, y):
            if 85<y<160 and (15<x<540 and 0<(x-15)%90<75):
                return ["a","b","c","d","e","f"][(x-15)//90]
            elif 190<y<265 and 15<x<540:
                return ["A","B","C","D","E","F"][(x-15)//90]
            else:
                return ""
        self.jouer(lettre(event.x, event.y))
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

            self.current_agent = self.agent1 if self.p.joueur1 else self.agent2

            if isinstance(self.current_agent, HumanAgent):
                # Si c'est un joueur humain, attendez qu'il fasse un mouvement via l'interface graphique
                pass
            else:
                # Si c'est un agent IA, faites-le jouer automatiquement
                action = self.current_agent.choose_action(state, available_actions)
                reward = self.p.coup(action)
                next_state = self.p.get_state()
                next_actions = self.p.get_available_actions()
                self.current_agent.learn(state, action, reward, next_state, next_actions)
                self.update_ui()
                self.after(100, self.play_with_agents)  # Continuez à jouer après un court délai
        else:
            # Si le jeu est terminé, vérifiez s'il y a égalité
            if self.p.score[0] == self.p.score[1]:
                # Affichez un message indiquant l'égalité
                self.id_couronne = self.canvas.create_text(555/2, 175, text="Égalité!", font=('Helvetica', 20), fill='gold')
                # Ajoutez un bouton "Rejouer" à la fin du jeu
                self.replay_button = Button(self, text="Rejouer", command=self.replay_game)
                self.replay_button.pack(pady=20)


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
        
    def couronne(self):                     
        x = 110
        y = 325 if self.p.vainqueur == 1 else 45 

        # Vérifiez s'il y a égalité
        if self.p.score[0] == self.p.score[1]:
            # Affichez un message indiquant l'égalité
            self.id_couronne = self.canvas.create_text(555/2, 175, text="Égalité!", font=('Helvetica', 20), fill='gold')
        else:
            # Sinon, affichez la couronne à côté du vainqueur
            self.id_couronne = self.canvas.create_polygon(x, y, x, y-25, x+6, y-7, x+12, y-25, x+18, y-7, x+24, y-25, x+30, y-7, x+36, y-25, x+36, y, fill='gold')
        
        # Ajoutez un bouton "Rejouer" à la fin du jeu
        self.replay_button = Button(self, text="Rejouer", command=self.replay_game)
        self.replay_button.pack(pady=20)


    def update_ui(self):
        # Mettre à jour l'interface graphique après chaque action
        self.ecrire_scores((self.p.score[0], self.p.score[1]))
        self.ecrire_nombres(self.p.liste)
        self.affiche_joueur()
        if self.p.vainqueur:
            self.couronne()
            print(self.p.vainqueur)


if __name__ == '__main__':
    Application().mainloop()
