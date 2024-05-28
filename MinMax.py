import numpy as np
import random

class MinMaxNode():

    def __init__(self, game, state) -> None:
        self.game = game
        self.state = state
        self.childs = {}
        self.file = ""

        '''
        state.is_over()
        state.legal_moves() -> liste des coups légaux
        state.current_player
        state.play_at()
        state.clone()
        state.evaluation()
        game.max_player

        '''

    def minimax(self, state, max_player, depth: int, print_tree=False):
        if depth == 0 or state.is_over():
            return (None, state.evaluation(max_player))
        if state.current_player == max_player:
            best_score = np.NINF
            legal_moves = state.legal_moves()
            random.shuffle(legal_moves)
            for move in legal_moves:
                tmp_state = state.clone()
                tmp_state.play_at(move)
                score = self.minimax(tmp_state, max_player, depth - 1)[1]
                if score > best_score:
                    best_score = score
                    best_move = move
        else:
            best_score = np.Inf
            legal_moves = state.legal_moves()
            random.shuffle(legal_moves)
            for move in legal_moves:
                tmp_state = state.clone()
                tmp_state.play_at(move)
                score = self.minimax(tmp_state, max_player, depth - 1)[1]
                if score < best_score:
                    best_score = score
                    best_move = move
        if print_tree:
            file = ""
            for i in range(depth):
                file += "    "
            file += f"({best_move}, {best_score})\n"
            print(file)
        return (best_move, best_score)
    
    def biased_simulation(self, state, max_player, depth: int, bias, print_tree=False):
        #bias=1 -> totalement aléatoire, bias=0 -> minmax normal
        if depth == 0 or state.is_over():
            return (None, state.evaluation(max_player))
        if state.current_player == max_player:
            legal_moves = state.legal_moves()
            move_list = []
            for move in legal_moves:
                tmp_state = state.clone()
                tmp_state.play_at(move)
                score = self.minimax(tmp_state, max_player, depth - 1)[1]
                move_list.append((score, move))
            best_moves = sorted(move_list, reverse=True)[:int(bias*len(move_list))+1]
            rand_best_score, rand_best_move = random.choice(best_moves)
        else: #joueur min
            legal_moves = state.legal_moves()
            move_list = []
            for move in legal_moves:
                tmp_state = state.clone()
                tmp_state.play_at(move)
                score = self.minimax(tmp_state, max_player, depth - 1)[1]
                move_list.append((score, move))
            best_moves = sorted(move_list, reverse=True)[:int(bias*len(move_list))+1]
            rand_best_score, rand_best_move = random.choice(best_moves)
        return (rand_best_move, rand_best_score)


