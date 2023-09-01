import random
from math import log, sqrt
from go import *
import time

class Node():

    def __init__(self, state):
        self.game = Go()
        self.weight = [0,0]
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
        #print(len(self.game.legal_moves(self.state)))
        return len(self.enfants) < len(self.game.legal_moves(self.state))

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
        new_state = self.game.play_mct(noeud.state, move, noeud.state.current_player)
        return noeud.add_child(move, new_state)

    def random_move(self, state):
        legal_moves = self.game.legal_moves(state)
        return legal_moves[random.randint(0,len(legal_moves)-1)]

    def selection(self, node):
        clock = time.clock_gettime(0)
        if not node.is_feuille():
            # print(self)
            return self.selection(node.best_child())
        #print ("selection: ", time.clock_gettime(0) - clock)
        return node

    def expension(self, noeud):
        legal_moves = self.game.legal_moves(noeud.state)
        random.shuffle(legal_moves)
        #print(f'Found {len(legal_moves)} legal moves')
        if not self.game.is_over(noeud.state):
            for move in legal_moves:
                if not (move in noeud.enfants.keys()):
                    self.new_child(noeud, move)
                    self.simulation(noeud.enfants[move])
                    break
        else:
            self.back_propagation(noeud, noeud.state)     #if there are no legal moves, skips expension and simulation

    def simulation(self, noeud):
        clock = time.clock_gettime(0)
        nv_state = noeud.state.clone()
        if not self.game.is_over(nv_state):
            sim = self.game.rand_simulation(nv_state)
        else:
            sim = nv_state
        #print(sim)
        #print ("simulation: ", time.clock_gettime(0) - clock)
        self.back_propagation(noeud, sim)

    def back_propagation(self, noeud, state):
        clock = time.clock_gettime(0)
        winner = self.game.winner(state)
        def _bp_rec(noeud):
            noeud.weight[1] += 1
            if noeud.state.current_player != winner:          # == -> !=
                noeud.weight[0] += 1
            if not noeud.is_racine():
                _bp_rec(noeud.parent)
        _bp_rec(noeud)
        #print ("back propagaiton: ", time.clock_gettime(0) - clock)

    def tree_search(self, root):
        self.expension(self.selection(root))

    def choose_best_node(self):
        best = (None, -1)
        for enf in self.root.enfants.values():
            if enf.weight[1] > best[1]:
                best = (enf, enf.weight[1])
        return (best[0], list(self.root.enfants.keys())[list(self.root.enfants.values()).index(best[0])])  #(node, move)

    def new_move(self, search_depth):
        clock = time.clock_gettime(0)
        for i in range(search_depth):
            self.tree_search(self.root)
            if i%100 == 0:
                print(i)
        best_node = self.choose_best_node()
        self.game._mct_move(best_node[0].state, best_node[1])
        #self.game.play_at(self.root.state, best_node[1])
        self.pretty_print()
        self.root = best_node[0]
        self.game.board = self.root.state
        #print('root state: ', self.root.state, '\n', self.root.state.current_player)
        print("new move: ", time.clock_gettime(0) - clock)
    
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
    
    def _pretty_print(self, node, acc, file):
        file.write("\n")
        for i in range(acc):
            file.write("  ")
        file.write("(")
        file.write(str(node))
        if len(node.enfants) > 0:
            for enf in node.enfants.values():
                self._pretty_print(enf, acc+1, file)
        file.write(")")

    def pretty_print(self):
        file = open("tree.lsp", "w")
        self._pretty_print(self.root, 0, file)

    def __str__(self) -> str:
        return str(f'root = {self.root}')
