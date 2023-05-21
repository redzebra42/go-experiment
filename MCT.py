import random
from go import *
import copy

class Node():

    def __init__(self, state):
        self.weight = [0,0]
        self.state = state
        self.enfants = []
        self.parent = None
        self.depth = 0              #pair depth is 'w' and odd is 'b'

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

    def __init__(self, game):
        self.arbre = Node(game().state)
        self.game = game
        '''
        games class (Go(state) or TTT(state)) with the following functions:
        play(coord: tuple) -> None
        play_random() -> None
        legal_moves() -> tuple list (with coords of legal moves)
        is_over() -> bool
        winner() -> str (player)
        player_to_depth(player: str) -> int (0 or 1)
        '''

    def selection(self, noeud):
        if not noeud.is_feuille():
            i = random.randrange(len(noeud.enfants))
            return self.selection(noeud.enfants[i])
        return noeud
    
    def expension(self, noeud):
        legal_moves = self.game().legal_moves()
        if legal_moves != []:
            for coord in legal_moves:
                new_game = self.game(noeud.state)
                nv_noeud = Node(new_game.state)
                new_game.play(coord)
                new_game.print_ttt()           #debug is here
                nv_noeud.weight = [0,0]
                nv_noeud.parent = noeud
                nv_noeud.depth = noeud.depth + 1
                noeud.enfants.append(nv_noeud)
                nv_noeud.state = new_game.state
            self.simulation(noeud.enfants[random.randint(0,len(noeud.enfants)-1)])
        else:
            self.back_propagation(noeud)     #if there are no legal moves, skips expension and simulation


    def simulation(self, noeud):
        if not self.game().is_over():
            new_game = self.game(noeud.state)
            nv_noeud = Node(new_game.state)
            new_game.game.play_random()
            nv_noeud.weight = [0,0]
            nv_noeud.parent = noeud
            nv_noeud.depth = noeud.depth + 1   
            noeud.enfant.append(nv_noeud)
            nv_noeud.state = new_game.state
            self.simulation(nv_noeud)
        else:
            self.back_propagation(noeud)

    def back_propagation(self, noeud):
        winner = self.game().winner()
        def _bp_rec(noeud):
            noeud.weight[1] += 1
            if noeud.depth % 2 == self.game().player_to_depth(winner):
                noeud.weight[0] += 1
            if not noeud.is_racine():
                _bp_rec(noeud.parent)
        _bp_rec(noeud)
    
    def tree_search(self, arbre):
        self.expension(self.selection(arbre))

