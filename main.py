# coding:utf-8

"""
Auteur : Julian FERRARINI
Auteur : Marco GILLES
"""

from Trou import Trou
from Plateau import Plateau
from Joueur import Joueur
from regex_pattern_valid import extract_case_number, extract_couleur

import random
import time

random.seed(time.time())

j1 = Joueur(pair=True)
j2 = Joueur(pair=False)

trous = []

for i in range(1, 17):
    trous.append(Trou(i, 2, 2))

plateau = Plateau([j1, j2], trous)

numero_tour = 1

while len(list(filter(lambda j: j.score >= 32, plateau.joueurs))) <= 0:
    print(plateau.trous)
    print(plateau.joueurs)

    joueur = plateau.joueurs[numero_tour%2]

    if (numero_tour%2 == 1):
        # L'IA
        ### TEMPORARY FOR TESTING, TO REMOVE WHEN DONE IMPLEMENTING IA
        
        # Choisir un trou pair random
        # Choisir la couleur de graine rouge ou bleu
        numero_trou = random.randrange(1, 16, 2)
        couleur = "R" if random.randrange(1, 3) == 1 else "B"
        action = f"{numero_trou}{couleur}"
        while not plateau.valid_action(action, joueur):
            numero_trou = random.randrange(1, 16, 2)
            couleur = "R" if random.randrange(1, 3) == 1 else "B"
            action = f"{numero_trou}{couleur}"
        print(f"{numero_trou}{couleur}")
    else:
        # ACTION À JOUER DANS LA CONSOLE
        action = input("Indiquez l'action à jouer : ")
        while not plateau.valid_action(action, joueur):
            action = input("Indiquez l'action à jouer : ")

    # Donne l'action à réaliser au plateau
    plateau.play_action(action, plateau.joueurs[numero_tour%2])

    # Incrementation du tour
    numero_tour += 1


gagnant = list(filter(lambda j: j.score >= 32, plateau.joueurs))[0]
string_pair = "pair" if gagnant.pair else "impair"
print(f"Le joueur {string_pair} est gagnat avec {gagnant.score} graines")