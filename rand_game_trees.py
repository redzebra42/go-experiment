import random
import math

global_size = 7

'''
game class that has the following functions:
legal_moves(state)
play_at(state, move)
is_over(state)
winner(state)
rand_simulation(state)
play_mct()

state class with the following functions:
curr_player()
clone()
'''


class RGTstate():

    def __init__(self, position=(0, 0), best_move=random.randint(1, math.factorial(global_size)), board_size=global_size) -> None:
        self.board_size = board_size
        self.best_move = best_move
        self.position = position
        self.tree = {(0, 0):0}
        self.init_tree()

    def init_tree(self):
        #dictionnary with the values of the tree's nodes (best path values are initialized here and random values will be added when calculating a score)
        for pos in self.path(self.best_move):
            self.tree[pos] = 1

    def update_tree(self, path):
        for pos in path:
            if not (pos in self.tree.keys()) :
                self.tree[pos] = random.randint(-10,10)/10

    def path(self, destination:int):
        nb_tot_moves = (math.factorial(self.board_size))
        frac = destination/nb_tot_moves
        path = []
        for i in range(self.board_size - 1):
            largeur = nb_tot_moves/math.factorial(self.board_size - i - 1)
            j = 0
            while j/largeur < frac:
                j += 1
            path.append((i + 1, j))
        return path
    
    def enfants(self, node) -> list:
        enf_list = []
        for i in range(self.board_size - node[0]):
            enf_list.append((node[0] + 1, node[1] * (self.board_size - node[0]) + i))
        return enf_list


    def curr_player(self):
        return self.position[0] % 2

    def clone(self):
        return RGTstate(self.position, self.best_move, self.board_size)

class RGT():
    """
    game tree represented by nodes with coordinates (depth, index) with depth of root = 0 and indexes 
    starting at 1 from left up to board_size!/(totaldepth-depth)! 
    """
    def __init__(self, state=RGTstate()) -> None:
        self.state = state

    def legal_moves(self, state):
        return state.enfants(state.position)

    def play_at(self, state, move):
        state.position = move

    def is_over(self, state):
        return state.position[0] == state.board_size - 1

    def winner(self, state):
        #TODO peut etre switch les valeurs du gagnant (ou y reflechir au moins) on rappelle que le score 
        #d'une case est positif si elle est bénéfique au joueur 1 (ou 0 mais faut se décider) et ce pour tout noeud.
        if self.is_over(state):
            path = state.path(state.position[1])
            state.update_tree(path)
            res = 0
            for pos in path:
                res += state.tree[pos]
            if res > 0:
                return 1
            else:
                return 0
        else:
            raise RuntimeError

    def rand_simulation(self, state):
        pass

    def play_mct(self):
        pass

    def _tree_dict_to_list(self):
        node_list = [[] for i in range(self.state.board_size)]
        for i in range(self.state.board_size):
            for node in self.state.tree:
                node_list[i].append(node[1])
        return node_list
    
    def _pretty_print_rec(self, node, file):
        if node[0] != 0:
            file.write("\n")
            for i in range(node[0]):
                file.write("    ")
        else:
            file.write(str(self.state.tree) + "\n")
        file.write(f"({node[0]}/{node[1]}/{self.state.tree[node]})")
        for enf in self.state.enfants(node):
            if enf in self.state.tree:
                self._pretty_print_rec(enf, file)
        
    
    def pretty_print(self, file):
        '''prints depth/position/value for each nodes with a value'''
        #TODO doesn't work yet, could try a non-recursive approach, or just give up, this function doesn't really matters anyways...
        self._pretty_print_rec((0, 0), file)
        
if __name__ == "__main__":
    pos = (3, 5)
    state = RGTstate(pos)
    rgt = RGT(state)

    print(rgt.legal_moves(state))
    rgt.play_at(state, (4,18))
    print(rgt.legal_moves(state))
    print(rgt.is_over(state))
    rgt.play_at(state, (6,34))
    print(rgt.legal_moves(state))
    print(rgt.is_over(state))
    print(state.best_move)
    print(state.path(state.best_move))
    print(rgt.winner(state))
    print(len(state.tree))
    print(rgt.state.enfants((1,3)))
    rgt.pretty_print(open("RGT_tree.lsp", "w"))