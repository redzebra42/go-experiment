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

    def is_feuille(self):
        return self.enfants == []

    def is_racine(self):
        return self.parent == None


class MCT():

    def __init__(self, game):
        self.arbre = Node(game)
        self.game = game         #game class (Go() or TTT()) that has play(), play_random(), legal_moves(), is_over(), winner(), player_to_depth() functions

    def selection(self, noeud):
        if not noeud.is_feuille():
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
        winner = noeud.game.winner()
        def _bp_rec(noeud):
            noeud.weight[1] += 1
            if noeud.depth % 2 == noeud.game.player_to_depth(winner()):
                noeud.wieght[0] += 1
            if not noeud.is_racine():
                _bp_rec(noeud.parent)
        _bp_rec(noeud)

