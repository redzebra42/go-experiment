import random
from go import *

class Node():

    def __init__(self, valeur):
        self.weight = None
        self.valeur = valeur
        self.enfants = []
        self.parent = None
        self.depth = 0              #pair depth is 'w' and odd is 'b'

    def ajouter_noeud(self, noeud, valeur):
        nv_noeud = Node(valeur)
        nv_noeud.weight = (0,1)
        nv_noeud.parent = noeud
        nv_noeud.depth = noeud.depth + 1
        noeud.enfant.append(nv_noeud)

    def is_feuille(self,noeud):
        return noeud.enfants == []

    def is_racine(self, noeud):
        return noeud.parent == None


class MCT():

    def __init__(self, goban):
        self.arbre = Node(goban)

    def selection(self, arbre):
        noeud = arbre.noeud
        if not Node.is_feuille(noeud):
            i = random.randrange(len(noeud.enfant))
            self.selection(noeud.enfant[i])
        return noeud

    def back_propagation(self, noeud):
        if not Node.is_racine(noeud):
            #TODO function that determines if the game is over, and who won
            pass
