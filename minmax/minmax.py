from copy import deepcopy
from game import Plateau, Joueur, Trou
from minmax.Node import Node
from time import time
from sys import maxsize
minsize = -maxsize - 1

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
    # la construction du graph prend beaucoup de temps
    initial_node.relations = build_tree(initial_node, plateau_copy, joueur, depth, joueur)
    # MinMax prend du temps mais moins que build_tree
    best_move = minmax(initial_node, depth, minsize, maxsize, maximise=True)
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
    nodes = []

    for coup in coups:
        node_coup = Node(action=coup, value=0, relations=[])

        # Copy du plateau pour ne pas le modifier pour les autres instances de build_tree
        copy_plateau = deepcopy(plateau)
        joueur, next_player = (copy_plateau.joueurs[0], copy_plateau.joueurs[1]) if copy_plateau.joueurs[0].pair==joueur.pair else (copy_plateau.joueurs[1], copy_plateau.joueurs[0])

        copy_plateau.play_action(coup, joueur)

        # Evaluation de la node
        node_coup.value = eval_node(copy_plateau)

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

def eval_node(plateau: Plateau) -> int:
    """
    @arg plateau, nouveau plateau après l'action
    @return score, retourne un score positif ou negatif en fonction de comment ça impacte notre joueur
    """

    # Evaluation simple, en fonction des scores des joueurs
    score = 0
    score += plateau.joueurs[0].score
    score += plateau.joueurs[1].score

    # TODO Complexification de l'évaluatio n du score, en fonction des cases qui ont été vidé, et que l'impact de l'évolution des scores des joueurs sur la notation ne soit pas linéaire

    return score

def minmax(node: Node, depth: int, alpha: int, beta: int, maximise=True) -> int:

    # On ne va pas plus bas on retourne la valeur
    if(depth==0):
        return node.value

    if maximise:
        maxEval = minsize
        for child in node.relations:
            valuation = minmax(child, depth-1, alpha, beta, maximise=not maximise)
            maxEval = max(valuation, maxEval)
            alpha = max(valuation, alpha)
            if(beta <= alpha):
                break
        node.value = maxEval
        return maxEval
    else:
        minEval = maxsize
        for child in node.relations:
            valuation = minmax(child, depth-1, alpha, beta, maximise=not maximise)
            minEval = min(valuation, minEval)
            beta = min(valuation, beta)
            if (beta<=alpha):
                break
        node.value = minEval
        return minEval