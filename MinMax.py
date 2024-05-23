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

    def minimax(self, state, depth: int, print_tree=False):
        if depth == 0 or state.is_over():
            return (None, state.evaluation())
        if state.current_player == state.max_player:
            best_score = np.NINF
            legal_moves = state.legal_moves()
            random.shuffle(legal_moves)
            for move in legal_moves:
                tmp_state = state.clone()
                tmp_state.play_at(move)
                score = self.minimax(tmp_state, depth - 1)[1]
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
                score = self.minimax(tmp_state, depth - 1)[1]
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

    def AlphaBeta(self, depth, alpha, beta):
        if self.state.is_over() or depth == 0:
            return self.state.evaluation()
        for move in self.state.legal_moves():
                tmp_state = self.state.clone()
                tmp_state.play_at(move)
                score = -tmp_state.AlphaBeta(depth - 1, -beta, -alpha)
                if score >= alpha:
                    alpha = score
                    best_move = move
                    if alpha >= beta:
                        break
        return best_move

            

