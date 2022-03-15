from copy import deepcopy
from game import Plateau, Joueur, Trou
from minmax.Node import Node
from time import time

def predict_action(plateau: Plateau, joueur: Joueur, depth=4) -> str:
    """
    @arg plateau, l'état du plateau actuel
    @arg joueur, le joueur pour lequel on veut prédire le coup
    @arg depth, la profondeur à laquelle il faut plonger dans l'arbre

    Sans parallélisation
    depth=3 -> 6 secondes
    depth=4 -> 106 secondes

    Applique l'algorithme minmax sur le jeu pour trouver le meilleur coup à jouer pour le bot
    Retourne l'action à jouer recommandé par le bot
    """

    # Construit l'arbre
    initial_node = Node(action="", value=0, relations=[])

    plateau_copy = deepcopy(plateau)

    start_time = time()
    initial_node.relations = build_tree(initial_node, plateau_copy, joueur, depth, joueur)
    end_time = time()
    print(f"Calculation for build_tree depth {depth} took {end_time-start_time} seconds")

    start_time = time()
    best_move = minmax(initial_node, depth, maximise=True)
    end_time = time()
    print(f"Calculation for mimmax depth {depth} took {end_time-start_time} seconds")

    print(f"Le score du meilleur move est de : {best_move}")

    action = ', '.join(list(map(lambda r: r.action, filter(lambda r: r.value==best_move, initial_node.relations))))

    return action

def build_tree(node: Node, plateau: Plateau, joueur: Joueur, depth: int, joueur_gagnant: Joueur) -> list[Node]:
    """
    @args node, node à partir de laquelle on doit générer les coups suivants
    @args plateau, plateau qui correspond à l'état du jeu pour la node
    @args joueur, le joueur qui doit jouer
    @args depth, la profondeur restante à évaluer
    @args joueur_gagnant, le joueur que le bot doit faire gagner
    @return Node, liste de node possible à pair de la node initial
    """
    coups = coup_possible(plateau, joueur)
    next_player = list(filter(lambda j: j.pair!=joueur.pair, plateau.joueurs))[0]
    nodes = []

    for coup in coups:
        node_coup = Node(action=coup, value=0, relations=[])

        # Copy du plateau pour ne pas le modifier pour les autres instances de build_tree
        copy_plateau = deepcopy(plateau)
        copy_plateau.play_action(coup, joueur)

        # Evaluation de la node
        node_coup.value = eval_node(plateau, copy_plateau, joueur_gagnant, node.value)

        # Construit les noeuds fils
        if(depth>0):
            node_coup.relations = build_tree(node_coup, copy_plateau, next_player, depth-1, joueur_gagnant)

        # Ajout des nodes dans la liste de retour
        nodes.append(node_coup)

    return nodes


def coup_possible(plateau: Plateau, joueur: Joueur) -> list[str]:
    coups_possibles = []
    if (joueur.pair):
        # Evaluer tous les coups possibles dans les cases pairs
        for i in range(2, 17, 2):
            trou = plateau.trous[i-1]
            if (trou.graine_Bleu > 0):
                coups_possibles.append(f"{i}B")
            if (trou.graine_Rouge > 0):
                coups_possibles.append(f"{i}R")
    else:
        # Evaluer tous les coups possibles dans les cases impairs
        for i in range(1, 16, 2):
            trou = plateau.trous[i-1]
            if (trou.graine_Bleu > 0):
                coups_possibles.append(f"{i}B")
            if (trou.graine_Rouge > 0):
                coups_possibles.append(f"{i}R")

    return coups_possibles

def eval_node(previous_plateau: Plateau, current_plateau: Plateau, joueur: Joueur, previous_score: int) -> int:
    """
    @arg previous_plateau, plateau original avant l'action
    @arg current_plateau, nouveau plateau après l'action
    @arg joueur, le joueur pour lequel on prédit le coup, pour lequel l'impact doit être positif ou négatif
    @return score, retourne un score positif ou negatif en fonction de comment ça impacte notre joueur
    """

    # Evaluation simple, en fonction des scores des joueurs
    score = previous_score

    score += current_plateau.joueurs[0].score - previous_plateau.joueurs[0].score
    score += current_plateau.joueurs[1].score - previous_plateau.joueurs[1].score

    # TODO Complexification de l'évaluatio n du score, en fonction des cases qui ont été vidé, et que l'impact de l'évolution des scores des joueurs sur la notation ne soit pas linéaire

    return score

def minmax(node: Node, depth: int, maximise=True) -> int:

    # On ne va pas plus bas on retourne la valeur
    if(depth==0):
        return node.value

    all_values = []
    for relation in node.relations:
        all_values.append(minmax(relation, depth-1, maximise=not maximise))

    node.value = max(all_values) if maximise else min(all_values)

    return node.value