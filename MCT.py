import random
from math import log, sqrt
import time


class MCT():

    def __init__(self, state, game) -> None:
        self.game = game
        self.weight = [0,0]  #[nb de fois gagné, nb de fois testé]
        self.state = state
        self.enfants = {}  #(key:move, value:MCT)
        self.parent = None
        self.depth = 0
        #la racine garde en mémoire le current_node de la partie
        self.current_node = None
        if self.is_racine():
            self.current_node = self

    def is_feuille(self) -> bool:
        #print(len(self.game.legal_moves(self.state)))
        return len(self.enfants) < len(self.state.legal_moves())

    def is_racine(self) -> bool:
        return self.parent == None
    
    def UTC(self):
        if self.parent != None:
            return (self.weight[0] / self.weight[1]) + sqrt(2 * log(self.parent.weight[1]) / self.weight[1])

    def best_child(self):
        best = (None, -1)
        # list = [(enf.weight[0] / enf.weight[1]) + sqrt(2) * sqrt(log(node.weight[1]) / enf.weight[1]) for enf in node.enfants.values()]
        for enf in self.enfants.values():
            score = (enf.weight[0] / enf.weight[1]) + sqrt(2 * log(self.weight[1]) / enf.weight[1])
            if (score > best[1]):
                best = (enf, score)
        return best[0]
    
    def best_child_with_eval_bias(self, eval, bias):
        best = (None, -1)
        # list = [(enf.weight[0] / enf.weight[1]) + sqrt(2) * sqrt(log(node.weight[1]) / enf.weight[1]) for enf in node.enfants.values()]
        for enf in self.enfants.values():
            score = (enf.weight[0] / enf.weight[1]) + sqrt(2 * log(self.weight[1]) / enf.weight[1]) + bias*enf.state.eval()
            if (score > best[1]):
                best = (enf, score)
        return best[0]
    
    '''
    game class that has the following functions:
    rand_simulation(state)
    play_mct()
    play_at(move)

    state class with the following functions:
    legal_moves()
    is_over()
    winner()
    curr_player()
    clone()
    '''

    def selection(self, eval_bias=False, eval=None, bias=1):
        if not eval_bias:
            return self.best_child()
        else:
            return self.best_child_with_eval_bias(eval, bias)

    def expension(self):
        '''ajoute aux enfants de self les nouveau noeuds correspondent a UN nouveu coup légal'''
        if not(self.state.is_over()):
            new_move = random.choice([e for e in self.state.legal_moves() if not e in self.enfants.keys()]) #liste des legal_moves sans les moves déja testés
            new_state = self.state.clone()
            self.game.play_at(new_state, new_move)
            new_node = MCT(new_state, self.game)
            new_node.parent = self
            self.enfants[new_move] = new_node
            return new_node
        else:
            return self
            raise RuntimeError #on ne devrait pas arriver a un état fini déja testé lors de la séléction

    def node_from_move(self, move):
        new_state = self.state.clone()
        self.game.play_at(new_state, move)
        new_node = MCT(new_state, self.game)
        new_node.parent = self
        self.enfants[move] = new_node
        return new_node

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
        if self.state.current_player != sim_winner:
            self.weight[0] += 1

    def tree_search(self, start_node, duration:int, iter:bool = False, nb_iter:int=100, eval_bias=False, eval=None, bias=1) -> tuple:
        if iter:
            clock = time.clock_gettime(0)
            for i in range(nb_iter):
                curr_node = start_node
                while not(curr_node.is_feuille()):
                    curr_node = curr_node.selection()
                curr_node = curr_node.expension()
                sim_res = curr_node.simulation()
                while not(curr_node.is_racine()):
                    curr_node.back_propagation(sim_res)
                    curr_node = curr_node.parent
                #on refait une dernière backpropagation pour la racine
                curr_node.back_propagation(sim_res)
                curr_node = curr_node.parent
            print("tree_search time: ", time.clock_gettime(0) - clock)
            print("mean time per search :", (time.clock_gettime(0) - clock) / nb_iter)
            return start_node.choose_best_node()                                                 #(node, move)
        else:
            start_time = time.clock_gettime(0)
            i = 0
            while duration > time.clock_gettime(0) - start_time:
                i += 1
                if i % 50 == 0:
                    print(i)
                curr_node = start_node
                while not(curr_node.is_feuille()):
                    curr_node = curr_node.selection(eval_bias, eval, bias)
                curr_node = curr_node.expension()
                sim_res = curr_node.simulation()
                while not(curr_node.is_racine()):
                    curr_node.back_propagation(sim_res)
                    curr_node = curr_node.parent
                #on refait une dernière backpropagation pour la racine
                curr_node.back_propagation(sim_res)
                curr_node = curr_node.parent
            print(i)
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
        root = self
        while not root.is_racine():
            root = root.parent
        self._pretty_print(root, 0, file)
        self.node_pretty_print()

    def node_pretty_print(self):
        file = open("node.lsp", "w")
        self._pretty_print(self, 0, file)
    
    def __str__(self) -> str:
        return str(f'weight = {self.weight}, size = {len(self.enfants)}, move = {self.state.prev_move}, eval = {self.UTC()}')

