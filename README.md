# Taquin-GBFS
Solveur du jeu du Taquin développé en Python, utilisant l’algorithme Greedy Best First Search (GBFS) afin de contourner le problème de l'explosion combinatoire inhérent aux méthodes exactes.

# Fonctionnalités
- Résolution automatique du jeu du Taquin grâce à l’algorithme Greedy Best First Search qui guide la recherche en se basant uniquement sur la distance de Manhattan comme fonction heuristique, permettant d’approcher rapidement la solution.
- Possibilité de jouer manuellement via une interface graphique en cliquant sur les cases du Taquin ou en saisissant les directions (`h`, `b`, `d`, `g` pour haut, bas, droite, gauche) puis en appuyant sur `Entrée` ou le bouton `déplacer` pour afin de bouger les pièces.
- L’algorithme GBFS permet d’afficher une solution approximative sous forme d’une séquence de mouvements menant à la résolution du casse-tête.

# Structure du Projet
- main.py : Contient le programme principal implémentant l'algorithme GBFS pour résoudre le jeu du Taquin avec une interface graphique interactive.

# Prérequis
- Python version 3.x
- Le package : colorama.

# Note
- Pour exécuter le projet, saisissez la commande `python main.py` dans votre terminal.
- Le problème du Taquin est un problème **NP-difficile**. Dans [un précédent projet](https://github.com/The-soulless12/Taquin-ASTAR), l’algorithme A* avait été utilisé avec succès sur des instances de petites tailles mais à cause de l’explosion combinatoire du nombre d’états à explorer, il ne permettait pas de trouver de solution en un temps raisonnable pour des grilles de taille 4x4 ou plus, la complexité croissant de manière exponentielle.
- Dans ce projet, une alternative a été proposée avec l’algorithme GBFS, qui ne garantit pas une solution optimale, mais permet d’obtenir une solution rapide et proche de l’optimum, tout en contournant les limitations des méthodes exactes.
