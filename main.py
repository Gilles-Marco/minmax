# coding:utf-8

"""
Auteur : Julian FERRARINI
Auteur : Marco GILLES
"""

from game.Trou import Trou
from game.Plateau import Plateau
from game.Joueur import Joueur
from game.regex_pattern_valid import extract_case_number, extract_couleur

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
    string_pair = "pair" if joueur.pair else "impair"
    print(f"C'est au joueur {string_pair} de jouer.")

    # PREDICTION
    

    action = input("Indiquez l'action à jouer : ")
    while not plateau.valid_action(action, joueur):
        action = input("Indiquez l'action à jouer : ")

    # Appliquer l'action à jouer
    plateau.play_action(action, plateau.joueurs[numero_tour%2])

    # Incrementation du tour
    numero_tour += 1


gagnant = list(filter(lambda j: j.score >= 32, plateau.joueurs))[0]
string_pair = "pair" if gagnant.pair else "impair"
print(f"Le joueur {string_pair} est gagnat avec {gagnant.score} graines")