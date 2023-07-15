import random
from math import log, sqrt
import numpy as np
#from go import *

class Node():

    def __init__(self, state):
        self.weight = [0,1]
        self.state = state
        self.enfants = {}
        self.parent = None
        self.depth = 0

    def add_child(self, coord, state):
        nv_noeud = Node(state)
        nv_noeud.weight = [0,0]
        nv_noeud.parent = self
        nv_noeud.depth = self.depth + 1
        self.enfants[coord] = nv_noeud
        return nv_noeud

    def is_feuille(self):
        return len(self.enfants) == 0

    def is_racine(self):
        return self.parent == None

    def best_child(self):
        best = (None, -1)
        # list = [(enf.weight[0] / enf.weight[1]) + sqrt(2) * sqrt(log(node.weight[1]) / enf.weight[1]) for enf in node.enfants.values()]
        for enf in self.enfants.values():
            score = (enf.weight[0] / enf.weight[1]) + sqrt(2 * log(self.weight[1]) / enf.weight[1])
            if (score > best[1]):
                best = (enf, score)
        return best[0]
    
    def __str__(self) -> str:
        return str(f'weight = {self.weight}, size = {len(self.enfants)}')

class MCT():

    def __init__(self, game, state):
        self.game = game
        self.root = Node(state)
        '''
        game class that has the following functions:
        legal_moves(state)
        play_at(state, move)
        is_over(state)
        winner(state)
        rand_simulation(state)
        state class with the following funcyions:
        curr_player()
        clone()
        '''

    def new_child(self, noeud, move):
        # new_state = noeud.state.clone()
        new_state = self.game.play_at(noeud.state, move)
        return noeud.add_child(move, new_state)

    def random_move(self, state):
        legal_moves = self.game.legal_moves(state)
        return legal_moves[random.randint(0,len(legal_moves)-1)]

    def selection(self, node):
        if not node.is_feuille():
            # print(self)
            return self.selection(node.best_child())
        return node

    def expension(self, noeud):
        legal_moves = self.game.legal_moves(noeud.state)
        print(f'Found {len(legal_moves)} legal moves')
        if not self.game.is_over(noeud.state):
            for move in legal_moves:
                self.new_child(noeud, move).weight[1] = 1
            self.simulation(noeud.enfants[random.choice(legal_moves)])
        else:
            self.back_propagation(noeud, noeud.state)     #if there are no legal moves, skips expension and simulation

    def simulation(self, noeud):
        nv_state = noeud.state.clone()
        if not self.game.is_over(nv_state):
            sim = self.game.rand_simulation(nv_state)
        else:
            sim = nv_state
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
        best = (None, -1)
        for enf in self.root.enfants.values():
            if enf.weight[1] > best[1]:
                best = (enf, enf.weight[1])
        return best[0]

    def new_move(self, search_depth):
        for i in range(search_depth):
            self.tree_search(self.root)
        self.root = self.choose_best_node()
        print('root state: ', self.root.state)
    
    def opponent_played(self, state):
        for node in [enf for enf in self.root.enfants.values()]:
            if node.state.ttt_board == state.ttt_board:
                self.root = node
        #TODO case where node isn't already created
    
    def set_played_move(self, coord):
        if coord in self.root.enfants:
            self.root = self.root.enfants[coord]
        else:
            self.root = self.new_child(self.root, coord)

    def __str__(self) -> str:
        return str(f'root = {self.root}')
