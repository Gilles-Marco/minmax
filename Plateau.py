from regex_pattern_valid import extract_case_number, extract_couleur

class Plateau:

    def __init__(self, joueurs, trous):
        
        self.joueurs = joueurs
        self.trous = trous

        print(self.trous)

    def valid_action(self, action, joueur):
        """
        Validate if the action requested by the player is valid
        Retourne True si l'action du joueur est valide
        Retourne False si l'action du joueur n'est pas valide et qu'il doit rejouer
        """

        case_number = int(extract_case_number(action))
        couleur = extract_couleur(action)

        if case_number is None:
            print("ERREUR: nous n'avons pas pu extraire le numéro de la case")
            return False
        if int(case_number) > 16 or int(case_number) < 1:
            print("ERREUR: le numéro de la case n'est pas compris entre 1 et 16") 
            return False
        if couleur is None:
            print("ERREUR: nous n'avons pas pu extraire la couleur des graines à récupérer")
            return False

        trou = self.trous[(case_number-1)%16]

        if joueur.pair and case_number%2 != 0:
            print("ERREUR: vous êtes le joueur pair et vous jouez une case impair")
            return False
        elif not joueur.pair and case_number%2 != 1:
            print("ERREUR: vous êtes le joueur impair et vous jouez une case pair")
            return False

        if couleur == "R" and trou.graine_Rouge <= 0:
            print("ERREUR: vous voulez récupérer les graines rouges d'une case qui n'en a pas")
            return False
        elif couleur == "B" and trou.graine_Bleu <= 0:
            print("ERREUR: vous voulez récupérer les graines bleus d'une case qui n'en a pas")
            return False

        return True



    def play_action(self, action, joueur):
        """
            Extrait le trou originel et l'action à jouer en fonction de la couleur des graines à récupérer
        """

        # Extrait le numero de la case selectionné dans l'action à éxécuter
        case_number = extract_case_number(action)
        # Extrait la couleur des graines à récupérer dans l'action à éxécuter
        graine_couleur = extract_couleur(action)

        # Convertit le numero du trou en index de liste python
        index_trou = (int(case_number)-1)%16

        # Récupération du trou
        trou = self.trous[index_trou]

        # Joue l'action en fonction de la couleur et du "trou originel"
        if(graine_couleur == "B"):
            dernier_trou = self.seme_graine_bleu(trou)
        else:
            dernier_trou = self.seme_graine_rouge(trou)

        # Capture les graines
        self.capture_graine(joueur, dernier_trou)

        #Check si un joueur n'est pas affamé
        affame = self.is_starved()
        if affame:
            self.donner_tte_graines(affame)

    def seme_graine_rouge(self, trou_originel):
        """
        Seme le nombre de graines rouges du trou originel dans chaque trou excepté le trou originel
        Et retire les graines rouges du trou originel
        Retourne la dernière case semée
        """
        dernier_trou = None
        for i in range(trou_originel.graine_Rouge):
            index_trou_a_semer = (trou_originel.numero+i)%16
            self.trous[index_trou_a_semer].graine_Rouge += 1
            dernier_trou = self.trous[index_trou_a_semer]
        trou_originel.graine_Rouge = 0
        return dernier_trou
    
    def seme_graine_bleu(self, trou_originel):
        """
        Seme 1 graine bleu dans les trous adverses * le nombre de graine bleus dans le trou
        Et retire les graines bleus du trou originel
        Retourne la dernière case semée
        """
        dernier_trou = None
        for i in range(trou_originel.graine_Bleu):
            index_trou_a_semer = (trou_originel.numero+(i*2))%16
            self.trous[index_trou_a_semer].graine_Bleu += 1
            dernier_trou = self.trous[index_trou_a_semer]
        trou_originel.graine_Bleu = 0
        return dernier_trou

    def capture_possible(self, dernier_trou):
        """
        La capture est possible si le nombre total de graines dans le trou est compris entre 2 et 3
        Retourne True si il y a entre 2 et 3 graines
        Retourne False s'il n'y a pas entre 2 et 3 graines
        """
        panier = 0
        panier += dernier_trou.graine_Bleu
        panier += dernier_trou.graine_Rouge
        
        return True if panier >= 2 and panier <= 3 else False
            

    def capture_graine(self, joueur, dernier_trou):
        """
        Si le trou appartient au joueur et qu'il y a 2 ou 3 graines bleu ou rouges dans le trou, le joueur les récupère (obligation)
        """
        while self.capture_possible(dernier_trou):
            # Récupère les graine du trou
            joueur.score += dernier_trou.graine_Bleu
            joueur.score += dernier_trou.graine_Rouge
            dernier_trou.graine_Bleu = 0
            dernier_trou.graine_Rouge = 0
            # Comme la capture a été possible on regarde si on peut récupérer les graines du trou d'avant
            dernier_trou = self.trous[(int(dernier_trou.numero)-2)%16]
 
    def is_starved(self):
        """
        Si un joueur ne peut plus jouer de coup car aucun de ces trous n'a de graines on considère qu'il "starve", il a alors perdu
        Retourne Joueur si un joueur est starve
        Retourne None si aucune joueur n'est starve
        """
        for joueur in self.joueurs:
            convert_pair_to_number = 0 if joueur.pair else 1
            trous_joueur = list(filter(lambda trou: trou.numero%2 == convert_pair_to_number, self.trous))
            trous = list(filter(lambda trou: trou.empty(), trous_joueur))
            if len(trous) == len(trous_joueur):
                return joueur
        return None

    def donner_tte_graines(self, joueur_affame):
        """
        Donne toutes les graines au joueur qui n'est pas affamé
        """
        gagnant = list(filter(lambda j: not j==joueur_affame, self.joueurs))[0]
        for trou in self.trous:
            gagnant.score += trou.graine_Bleu
            gagnant.score += trou.graine_Rouge
            trou.graine_Bleu = 0
            trou.graine_Rouge = 0

    def __repr__(self):
        return f"{len(self.joueurs)} joueurs ;; {len(self.trous)} trous"