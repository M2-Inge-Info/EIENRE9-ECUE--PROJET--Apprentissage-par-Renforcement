import tkinter as tk
from tkinter import messagebox


class AwaleGame:
    def __init__(self, master):
        self.master = master
        self.master.title("Jeu Awalé")

        # Initialisation des scores et du tour
        self.scores = [0, 0]
        self.current_player = 0  # 0 pour le joueur 1, 1 pour le joueur 2

        # Couleurs
        self.bg_color = "#F5DEB3"  # Couleur de fond beige
        self.hole_color = "#8B4513"  # Couleur marron pour les trous
        self.seed_color = "#DAA520"  # Couleur dorée pour les graines

        # Initialisation du plateau de jeu
        self.board = [4] * 12  # 12 trous avec 4 graines chacun

        # Création de l'interface
        self.create_ui()

    def create_ui(self):
        self.master.configure(bg=self.bg_color)

        # Cadre pour le plateau de jeu
        board_frame = tk.Frame(self.master, bg=self.bg_color)
        board_frame.pack(pady=20)

        # Création des trous
        self.hole_buttons = [None] * 12  # Initialise la liste avec 12 éléments None
        for i in range(11, -1, -1):  # Inverse l'ordre de création des trous
            hole = tk.Canvas(board_frame, width=60, height=60, bg=self.hole_color, highlightthickness=0)
            hole.grid(row=i//6, column=i%6, padx=10, pady=10)
            hole.bind("<Button-1>", lambda event, i=i: self.on_hole_click(i))
            self.hole_buttons[i] = hole  # Affecte le trou à l'index approprié
            self.draw_seeds(i)

        # Affichage du score
        self.score_label = tk.Label(self.master, text="Score: 0 - 0", bg=self.bg_color, font=("Arial", 16))
        self.score_label.pack(pady=20)


    def draw_seeds(self, hole_index):
        hole = self.hole_buttons[hole_index]
        hole.delete("seed")
        for i in range(self.board[hole_index]):
            x = 10 + (i % 4) * 15
            y = 10 + (i // 4) * 15
            hole.create_oval(x, y, x+10, y+10, fill=self.seed_color, tags="seed")

    def on_hole_click(self, hole_number):
        # Vérifie si c'est le bon joueur qui joue
        if (self.current_player == 0 and hole_number > 5) or (self.current_player == 1 and hole_number < 6):
            return

        seeds = self.board[hole_number]
        self.board[hole_number] = 0

        # Distribution des graines dans le sens inverse des aiguilles d'une montre
        index = hole_number
        while seeds > 0:
            index = (index - 1) % 12
            self.board[index] += 1
            seeds -= 1

        # Vérifie si on peut capturer les graines de l'adversaire
        opponent_range = range(6, 12) if self.current_player == 0 else range(0, 6)
        captured_seeds = 0
        while index in opponent_range and 2 <= self.board[index] <= 3:
            captured_seeds += self.board[index]
            self.board[index] = 0
            index = (index - 1) % 12

        self.scores[self.current_player] += captured_seeds

        # Vérifie si l'adversaire a des graines dans son camp
        if sum(self.board[i] for i in opponent_range) == 0:
            # Si l'adversaire n'a pas de graines, vérifie si on peut lui en donner
            if sum(self.board[i] for i in range(6, 12) if i != hole_number) == 0:
                # Si on ne peut pas lui en donner, la partie est terminée
                self.end_game()
                return

        # Change de joueur
        self.current_player = 1 - self.current_player

        # Mise à jour de l'interface
        for i in range(12):
            self.draw_seeds(i)
        self.update_score_and_turn()

    def update_score_and_turn(self):
        self.score_label.config(text=f"Score: {self.scores[0]} - {self.scores[1]}")
        turn_label = "Joueur 1" if self.current_player == 0 else "Joueur 2"
        self.turn_label.config(text=f"Tour de {turn_label}")

    def end_game(self):
        # Fin de la partie par famine
        player_range = range(6, 12) if self.current_player == 0 else range(0, 6)
        opponent_range = range(0, 6) if self.current_player == 0 else range(6, 12)
        
        if sum(self.board[i] for i in player_range) == 0:
            # Si le joueur actuel n'a pas de graines dans son camp
            if sum(self.board[i] for i in opponent_range) == 0 or all(self.board[i] not in [2, 3] for i in opponent_range):
                # Si l'adversaire n'a pas de graines ou ne peut pas faire de prises
                self.scores[1 - self.current_player] += sum(self.board[i] for i in opponent_range)
                for i in opponent_range:
                    self.board[i] = 0

        # Fin de la partie par indétermination
        if all(val not in [2, 3] for val in self.board):
            self.scores[0] += sum(self.board[i] for i in range(0, 6))
            self.scores[1] += sum(self.board[i] for i in range(6, 12))
            for i in range(12):
                self.board[i] = 0

        # Mise à jour de l'interface pour afficher les scores finaux
        self.update_score_and_turn()

        # Affichage d'un message indiquant le gagnant
        winner = "Joueur 1" if self.scores[0] > self.scores[1] else "Joueur 2" if self.scores[1] > self.scores[0] else "Pas de gagnant (égalité)"
        tk.messagebox.showinfo("Fin de la partie", f"La partie est terminée !\n\n{winner} a gagné !")


if __name__ == "__main__":
    root = tk.Tk()
    game = AwaleGame(root)
    root.mainloop()
