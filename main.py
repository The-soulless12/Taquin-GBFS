import random
import heapq
from colorama import Fore, Style
import tkinter as tk
from tkinter import messagebox

def creer_taquin(taille):
    while True:
        valeurs = list(range(1, taille * taille)) + [0] 
        random.shuffle(valeurs)
        grille = [valeurs[i * taille:(i + 1) * taille] for i in range(taille)]
        
        if est_solvable(grille) and grille != [[(i * taille + j + 1) % (taille * taille) for j in range(taille)] for i in range(taille)]:
            return grille

def transposition(valeurs, N):
    valeurs_new = [N if v == 0 else v for v in valeurs]
    cible = sorted(valeurs_new)
    transpositions = 0
    index_map = {val: i for i, val in enumerate(valeurs_new)}  
    
    for i in range(len(valeurs_new)):
        while valeurs_new[i] != cible[i]: 
            cible_index = index_map[cible[i]]  
            valeurs_new[i], valeurs_new[cible_index] = valeurs_new[cible_index], valeurs_new[i]  
            index_map[valeurs_new[cible_index]] = cible_index 
            index_map[valeurs_new[i]] = i 
            transpositions += 1  
    
    return transpositions 

def permutations_case_vide(valeurs, taille):
    valeurs_new = [taille*taille if v == 0 else v for v in valeurs]
    index_vide = valeurs_new.index(taille*taille)  
    
    ligne = (index_vide) // taille
    colonne = (index_vide) % taille
    return ( 2*taille- 2 - ligne - colonne)

def est_solvable(grille):
    taille = len(grille)
    valeurs = [grille[i][j] for i in range(taille) for j in range(taille)]
    N = taille * taille  
    
    nb_transposition = transposition(valeurs, N)
    nb_permutations= permutations_case_vide(valeurs, taille)
    return (nb_transposition % 2) == (nb_permutations % 2) 

def afficher_taquin(grille):
    taille = len(grille)
    largeur = len(str(taille * taille - 1))
    separateur = "+" + ("-" * (largeur + 2) + "+") * taille
    
    for i, ligne in enumerate(grille):
        print(separateur)
        ligne_str = ""
        for j, cell in enumerate(ligne):
            if (i, j) in cases_cibles(grille):
                cell_str = f"{cell if cell != 0 else ' ' :>{largeur}}"
                ligne_str += f"| {Fore.RED}{cell_str}{Style.RESET_ALL} "
            else:
                ligne_str += f"| {cell if cell != 0 else ' ' :>{largeur}} "
        print(ligne_str + " |")
    print(separateur)

def trouver_case_vide(grille):
    for i, ligne in enumerate(grille):
        for j, valeur in enumerate(ligne):
            if valeur == 0:
                return i, j
    return None

def deplacer(grille, direction):
    taille = len(grille)
    x, y = trouver_case_vide(grille)
    
    mouvements = {
        "b": (x - 1, y),
        "h": (x + 1, y),
        "d": (x, y - 1),
        "g": (x, y + 1)
    }
    
    if direction in mouvements:
        nx, ny = mouvements[direction]
        if 0 <= nx < taille and 0 <= ny < taille:
            grille[x][y], grille[nx][ny] = grille[nx][ny], grille[x][y]

def cases_cibles(grille):
    taille = len(grille)
    x, y = trouver_case_vide(grille)
    cases = []

    mouvements = [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]
    for nx, ny in mouvements:
        if 0 <= nx < taille and 0 <= ny < taille:
            cases.append((nx, ny))

    return cases

def est_termine(grille):
    taille = len(grille)
    compteur = 1  
    for i in range(taille):
        for j in range(taille):
            if grille[i][j] != 0 and grille[i][j] != compteur:
                return False
            compteur += 1
    print("\nFélicitations, vous avez gagné !\n")
    return True

def copier_grille(grille):
    return [ligne[:] for ligne in grille]

def trouver_voisins(grille):
    voisins = []
    taille = len(grille)
    x, y = trouver_case_vide(grille)

    mouvements = {
        'bas': (x - 1, y),
        'haut': (x + 1, y),
        'droite': (x, y - 1),
        'gauche': (x, y + 1)
    }

    for direction, (nx, ny) in mouvements.items():
        if 0 <= nx < taille and 0 <= ny < taille:
            nouvelle_grille = copier_grille(grille)
            nouvelle_grille[x][y], nouvelle_grille[nx][ny] = nouvelle_grille[nx][ny], nouvelle_grille[x][y]
            voisins.append((direction, nouvelle_grille))

    return voisins

def heuristique(grille):
    taille = len(grille)
    h = 0
    for i in range(taille):
        for j in range(taille):
            valeur = grille[i][j]
            if valeur != 0:
                i_cible = (valeur - 1) // taille
                j_cible = (valeur - 1) % taille
                h += abs(i - i_cible) + abs(j - j_cible)
    return h

def greedy_best_first(grille_depart):
    queue = []
    visited = set()
    heapq.heappush(queue, (heuristique(grille_depart), [], grille_depart))

    while queue:
        _, chemin, etat = heapq.heappop(queue)

        etat_tuple = tuple(tuple(row) for row in etat)
        if etat_tuple in visited:
            continue
        visited.add(etat_tuple)

        if est_termine(etat):
            return chemin

        for direction, voisin in trouver_voisins(etat):
            voisin_tuple = tuple(tuple(row) for row in voisin)
            if voisin_tuple not in visited:
                heapq.heappush(queue, (heuristique(voisin), chemin + [direction], voisin))
    
    return []

class TaquinApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Taquin")

        self.taille = 3
        self.taquin = creer_taquin(self.taille)

        self.frame = tk.Frame(self.root)
        self.frame.pack()

        self.labels = [[None for _ in range(self.taille)] for _ in range(self.taille)]
        self.create_buttons()

        self.entry = tk.Entry(self.root, font=("Courier", 14))
        self.entry.pack()

        self.submit_button = tk.Button(self.root, text="Déplacer", command=self.deplacer_utilisateur)
        self.submit_button.pack()

        self.result_button = tk.Button(self.root, text="Trouver solution", command=self.trouver_solution)
        self.result_button.pack()

        self.root.bind('<Return>', self.deplacer_utilisateur_entree)

        self.recommencer_button = tk.Button(self.root, text="Nouveau Taquin", command=self.reinitialiser)
        self.recommencer_button.pack()

        self.solution_fenetre = None

        self.root.resizable(False, False)

    def create_buttons(self):
        for i in range(self.taille):
            for j in range(self.taille):
                label = tk.Label(self.frame, text=self.taquin[i][j] if self.taquin[i][j] != 0 else '',
                                 width=4, height=2, relief="solid", font=("Courier", 14))
                label.grid(row=i, column=j, padx=5, pady=5)
                self.labels[i][j] = label
                label.bind("<Button-1>", lambda event, x=i, y=j: self.clic_piece(x, y))
        self.update()

    def update(self):
        for i in range(self.taille):
            for j in range(self.taille):
                value = self.taquin[i][j]
                if value == 0:
                    self.labels[i][j].config(text="", bg="white")
                else:
                    self.labels[i][j].config(text=str(value), bg="lightsalmon")

    def clic_piece(self, i, j):
        x, y = trouver_case_vide(self.taquin)
        
        if abs(i - x) + abs(j - y) == 1:
            self.taquin[x][y], self.taquin[i][j] = self.taquin[i][j], self.taquin[x][y]
            self.update()
            if est_termine(self.taquin):
                messagebox.showinfo("Victoire", "Félicitations, vous avez gagné !")

    def deplacer_utilisateur(self, event=None):
        direction = self.entry.get()
        if direction in ['h', 'b', 'd', 'g']:
            deplacer(self.taquin, direction)
            self.update()
            if est_termine(self.taquin):
                messagebox.showinfo("Victoire", "Félicitations, vous avez gagné !")
        self.entry.delete(0, tk.END)

    def deplacer_utilisateur_entree(self, event):
        self.deplacer_utilisateur()

    def trouver_solution(self):
        sequence_solution = greedy_best_first(self.taquin)
        if self.solution_fenetre:
            self.solution_fenetre.destroy()
        
        self.solution_fenetre = tk.Toplevel(self.root)
        self.solution_fenetre.title("Solution")
        frame_scroll = tk.Frame(self.solution_fenetre)
        frame_scroll.pack(padx=20, pady=20, fill=tk.BOTH, expand=True)

        scrollbar = tk.Scrollbar(frame_scroll)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        text_box = tk.Text(frame_scroll, wrap=tk.WORD, yscrollcommand=scrollbar.set, font=("Courier", 14), height=20, width=50)
        text_box.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=text_box.yview)

        text_box.insert(tk.END, "Voici la solution du taquin :\n\n" + "\n".join(sequence_solution))
        text_box.config(state=tk.DISABLED)


        fermer_button = tk.Button(self.solution_fenetre, text="Fermer", command=self.solution_fenetre.destroy)
        fermer_button.pack(pady=10)

    def reinitialiser(self):
        if self.solution_fenetre: 
            self.solution_fenetre.destroy()
            self.solution_fenetre = None

        self.taquin = creer_taquin(self.taille)  
        self.update() 

if __name__ == "__main__":
    root = tk.Tk()
    app = TaquinApp(root)
    root.mainloop()