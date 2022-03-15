# coding:utf-8

"""
Auteur : Julian FERRARINI
Auteur : Marco GILLES
"""

from game.Trou import Trou
from game.Plateau import Plateau
from game.Joueur import Joueur
from minmax.minmax import predict_action
import re

import random
import time

# Initialization du jeu
random.seed(time.time())

j1 = Joueur(pair=True)
j2 = Joueur(pair=False)

trous = []

for i in range(1, 17):
    trous.append(Trou(i, 2, 2))

plateau = Plateau([j1, j2], trous)

numero_tour = 1

DEPTH = 2

# Quel joueur est controlé par l'humain
pattern_impair = re.compile(r"^\s*impair\s*", re.I+re.M)
pattern_pair = re.compile(r"^\s*pair\s*$", re.I+re.M)
joueur_demande = input("Êtes-vous le joueur pair ou impair (pair/impair) : ")
is_joueur_pair = False
input_valid = False

while not input_valid:
    if (re.search(pattern_impair, joueur_demande)):
        is_joueur_pair = False
        input_valid = True
    elif (re.search(pattern_pair, joueur_demande)):
        is_joueur_pair = True
        input_valid = True
    else:
        joueur_demande = input("Êtes-vous le joueur pair ou impair (pair/impair) : ")

# Lancement du jeu
while len(list(filter(lambda j: j.score >= 32, plateau.joueurs))) <= 0:
    print(plateau.trous)
    print(plateau.joueurs)

    joueur = plateau.joueurs[numero_tour%2]
    string_pair = "pair" if joueur.pair else "impair"
    print(f"C'est au joueur {string_pair} de jouer.")

    # Joueur jouer par l'humain
    if (is_joueur_pair is joueur.pair):
        action = input("Indiquez l'action à jouer : ")
        while not plateau.valid_action(action, joueur):
            print("Action invalide...")
            action = input("Indiquez l'action à jouer : ")
    # Joueur joué par la machine
    else:
        action = predict_action(plateau, joueur, depth=DEPTH)
        while not plateau.valid_action(action, joueur):
            print("Action invalide par le bot")
            action = predict_action(plateau, joueur, depth=DEPTH)
            action = action.split(", ")
            action = random.choice(action)
        print(f"Le robot joue l'action {action}")

    # Appliquer l'action à jouer
    plateau.play_action(action, plateau.joueurs[numero_tour%2])

    # Incrementation du tour
    numero_tour += 1


gagnant = list(filter(lambda j: j.score >= 32, plateau.joueurs))[0]
string_pair = "pair" if gagnant.pair else "impair"
print(f"Le joueur {string_pair} est gagnat avec {gagnant.score} graines")