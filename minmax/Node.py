class Node:

    def __init__(self, action="", value=-1, relations=[]):
        self.relations = relations
        self.value = value
        self.action = action

    def __repr__(self):
        return f"{self.action} : {self.value}"