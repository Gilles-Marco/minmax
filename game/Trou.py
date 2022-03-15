class Trou:

    def __init__(self, numero, graine_Rouge, graine_Bleu):
        self.numero = numero
        self.graine_Rouge = graine_Rouge
        self.graine_Bleu = graine_Bleu

    def empty(self) -> bool:
        return True if self.graine_Bleu == 0 and self.graine_Rouge == 0 else False

    def __repr__(self) -> str:
        return f"Trou n°{self.numero}; graines rouges = {self.graine_Rouge} ; graines bleus = {self.graine_Bleu}"
