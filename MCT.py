import random
from math import log, sqrt
import numpy as np
#from go import *

def best_child(node):
    enfants = node.enfants
    L = [(enf.weight[0] / enf.weight[1]) + sqrt(2) * sqrt(log(node.weight[1]) / enf.weight[1]) for enf in node.enfants]
    return enfants[np.argmax(np.asarray(L))]

class Node():

    def __init__(self, state):
        self.weight = [0,1]
        self.state = state
        self.enfants = []
        self.parent = None
        self.depth = 0

    def ajouter_noeud(self, noeud, state):
        nv_noeud = Node(state)
        nv_noeud.weight = [0,0]
        nv_noeud.parent = noeud
        nv_noeud.depth = noeud.depth + 1
        noeud.enfants.append(nv_noeud)

    def is_feuille(self):
        return self.enfants == []

    def is_racine(self):
        return self.parent == None


class MCT():

    def __init__(self, game, state):
        self.game = game
        self.root = Node(state)
        '''
        games class (Go(state) or TTT(state)) with the following functions:
        play(coord: tuple) -> None
        play_random() -> None
        legal_moves() -> tuple list (with coords of legal moves)
        is_over() -> bool
        winner() -> str (player)
        player_to_depth(player: str) -> int (0 or 1)
        '''

    def new_child(self, noeud, move):
        new_state = noeud.state.clone()
        nv_noeud = Node(new_state)
        nv_noeud.weight = [0,0]
        nv_noeud.parent = noeud
        nv_noeud.depth = noeud.depth + 1
        noeud.enfants.append(nv_noeud)
        self.game.play(new_state, move)
        return nv_noeud

    def random_move(self, state):
        legal_moves = self.game.legal_moves(state)
        return legal_moves[random.randint(0,len(legal_moves)-1)]

    def selection(self, node):
        if not node.is_feuille():
            return self.selection(best_child(node))
        return node

    def expension(self, noeud):
        legal_moves = self.game.legal_moves(noeud.state)
        if not self.game.is_over(noeud.state):
            for move in legal_moves:
                self.new_child(noeud, move).weight[1] = 1
            self.simulation(noeud.enfants[random.randint(0,len(noeud.enfants)-1)])
        else:
            self.back_propagation(noeud, noeud.state)     #if there are no legal moves, skips expension and simulation

    def simulation(self, noeud):
        if not self.game.is_over(noeud.state):
            sim = self.game.rand_simulation(noeud.state)
        else:
            sim = noeud.state
        self.back_propagation(noeud, sim)

    def back_propagation(self, noeud, state):
        winner = self.game.winner(state)
        def _bp_rec(noeud):
            noeud.weight[1] += 1
            if noeud.state.curr_player != winner:          # == -> !=
                noeud.weight[0] += 1
            if not noeud.is_racine():
                _bp_rec(noeud.parent)
        _bp_rec(noeud)

    def tree_search(self, root):
        self.expension(self.selection(root))

    def choose_best_node(self):
        best = self.root.enfants[0]
        for enf in self.root.enfants:
            if enf.weight[1] > best.weight[1]:
                best = enf
        return(best)

    def new_move(self, search_depth):
        for i in range(search_depth):
            self.tree_search(self.root)
        self.root = self.choose_best_node()