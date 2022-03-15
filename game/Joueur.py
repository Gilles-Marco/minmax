class Joueur:

    def __init__(self, pair=True):
        
        self.pair = pair
        self.score = 0

    def __repr__(self) -> str:
        string_pair = "pair" if self.pair else "impair"
        return f"Joueur {string_pair} ; score : {self.score}"