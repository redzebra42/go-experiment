import random
from go import *
import copy

class Node():

    def __init__(self, valeur):
        self.weight = None
        self.valeur = valeur
        self.enfants = []
        self.parent = None
        self.depth = 0              #pair depth is 'w' and odd is 'b'

    def ajouter_noeud(self, noeud, valeur):
        nv_noeud = Node(valeur)
        nv_noeud.weight = (0,0)
        nv_noeud.parent = noeud
        nv_noeud.depth = noeud.depth + 1
        noeud.enfant.append(nv_noeud)

    def is_feuille(self, noeud):
        return noeud.enfants == []

    def is_racine(self, noeud):
        return noeud.parent == None


class MCT():

    def __init__(self, game):
        self.arbre = Node(game)
        self.game = game         #game class (Go() or TTT()) that has play(), play_random(), legal_moves(), is_over(), winner() functions

    def selection(self, arbre):
        noeud = arbre
        if not Node.is_feuille(noeud):
            i = random.randrange(len(noeud.enfant))
            return self.selection(noeud.enfant[i])
        return noeud
    
    def expension(self, noeud):
        for coord in self.game.legal_moves():
            nv_noeud = Node(noeud.game)
            nv_noeud.game.play(coord)
            nv_noeud.weight = (0,0)
            nv_noeud.parent = noeud
            nv_noeud.depth = noeud.depth + 1
            noeud.enfant.append(nv_noeud)

    def simulation(self, noeud):
        if not noeud.game.is_over():
            nv_noeud = Node(noeud.game)
            nv_noeud.game.play_random()   
            nv_noeud.weight = (0,0)
            nv_noeud.parent = noeud
            nv_noeud.depth = noeud.depth + 1   
            noeud.enfant.append(nv_noeud)
            self.simulation(nv_noeud)
        else:
            self.back_propagation(noeud)

    def back_propagation(self, noeud):
        if not noeud.is_racine(noeud):
            #TODO before this function: function that determines if the game is over, and who won
            pass
