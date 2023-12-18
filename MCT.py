import random
from math import log, sqrt
import time


class MCT():

    def __init__(self, state, game) -> None:
        self.game = game
        self.weight = [1,1]  #[nb de fois testé, nb de fois gagné]
        self.state = state
        self.enfants = {}  #(key:move, value:MCT)
        self.parent = None
        self.depth = 0

    def is_feuille(self) -> bool:
        #print(len(self.game.legal_moves(self.state)))
        return len(self.enfants) < len(self.state.legal_moves())

    def is_racine(self) -> bool:
        return self.parent == None

    def best_child(self):
        best = (None, -1)
        # list = [(enf.weight[0] / enf.weight[1]) + sqrt(2) * sqrt(log(node.weight[1]) / enf.weight[1]) for enf in node.enfants.values()]
        for enf in self.enfants.values():
            score = (enf.weight[0] / enf.weight[1]) + sqrt(2 * log(self.weight[1]) / enf.weight[1])
            if (score > best[1]):
                best = (enf, score)
        return best[0]
    
    
    '''
    game class that has the following functions:
    rand_simulation(state)
    play_mct()

    state class with the following functions:
    legal_moves()
    play_at(move)
    is_over()
    winner()
    curr_player()
    clone()
    '''

    def selection(self):
        return self.best_child()

    def expension(self):
        '''ajoute aux enfants de self les nouveau noeuds correspondent a tout les coups légaux '''
        if not(self.state.is_over()):
            for new_move in self.state.legal_moves():
                new_state = self.state.clone()
                self.game.play_at(new_state, new_move)
                new_node = MCT(new_state, self.game)
                new_node.parent = self
                self.enfants[new_move] = new_node
            return random.choice(list(self.enfants.values()))
        else:
            return self
            raise RuntimeError #on ne devrait pas arriver a un état fini déja testé lors de la séléction

    def simulation(self):
        '''renvois le vainqueur d'une simulation aléatoire a partir de l'état de self'''
        new_state = self.state.clone()
        self.game.rand_simulation(new_state)
        if new_state.is_over():
            return new_state.winner()
        else:
            raise RuntimeError #rand_simulation devrait aller jusqu'a la fin de la partie

    def back_propagation(self, sim_winner):
        '''update le poids d'un noeud selon le résultat de la simulation'''
        self.weight[1] += 1
        if self.state.current_player == sim_winner:
            self.weight[0] += 1

    def tree_search(self, start_node, duration:int, iter:bool = False, nb_iter:int=100):
        if iter:
            for i in range(nb_iter):
                curr_node = start_node
                while not(curr_node.is_feuille()):
                    curr_node = curr_node.selection()
                curr_node = curr_node.expension()
                sim_res = curr_node.simulation()
                while not(curr_node.is_racine()):
                    curr_node.back_propagation(sim_res)
                    curr_node = curr_node.parent
            return start_node.choose_best_node()
        else:
            start_time = time.clock_gettime(0)
            i = 0
            while duration > time.clock_gettime(0) - start_time:
                i += 1
                curr_node = start_node
                while not(curr_node.is_feuille()):
                    curr_node = curr_node.selection()
                curr_node = curr_node.expension()
                sim_res = curr_node.simulation()
                while not(curr_node.is_racine()):
                    curr_node.back_propagation(sim_res)
                    curr_node = curr_node.parent
            return start_node.choose_best_node()
        

    def choose_best_node(self):
        '''retourne l'enfant le plus visité du noeud self et le move associé'''
        best = (None, -1)
        for enf in self.enfants.values():
            if enf.weight[1] > best[1]:
                best = (enf, enf.weight[1])
        return (best[0], list(self.enfants.keys())[list(self.enfants.values()).index(best[0])])  #(node, move)
    
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
        root = self.root
        while not root.is_racine():
            root = root.parent
        self._pretty_print(root, 0, file)
        self.node_pretty_print()

    def node_pretty_print(self):
        file = open("node.lsp", "w")
        self._pretty_print(self.root, 0, file)
    
    def __str__(self) -> str:
        return str(f'weight = {self.weight}, size = {len(self.enfants)}, move = {self.state.two_previous_moves[0]}')

