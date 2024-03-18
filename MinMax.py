import numpy as np

class MinMaxNode():

    def __init__(self, game, state) -> None:
        self.game = game
        self.state = state
        self.childs = {}
        self.is_max = self.state.current_player == self.game.max_player

        '''
        state.is_over()
        state.legal_moves() -> liste des coups légaux
        state.current_player
        state.play_at()
        state.clone()
        state.evaluation()
        game.max_player

        '''

    def minimax(self, depth):
        best_move
        if self.state.is_over() or depth == 0:
            return self.state.evaluation()
        if self.is_max:
            best_score = np.NINF
            for move in self.state.legal_moves():
                tmp_state = self.state.clone()
                tmp_state.play_at(move)
                score = tmp_state.minimax(depth - 1)
                if score > best_score:
                    best_score = score
                    best_move = move
        else:
            best_score = np.Inf
            for move in self.state.legal_moves():
                tmp_state = self.state.clone()
                tmp_state.play_at(move)
                score = tmp_state.minimax(depth - 1)
                if score < best_score:
                    best_score = score
                    best_move = move
        return best_move
            

