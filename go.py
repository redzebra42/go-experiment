import board

class Go():


    def __init__(self):
        self.board = board.Board()
        self.current_player = 'w'
        self.turn = 0
        #self.previous_move = None
        self.komi = 6.5
        #self.captured_pieces = {'w': 0, 'b': 0}

    def hand_to_coord(self, hand):
        '''Convert a textual hand like c12 into coordinates like (2, 12).'''
        self.list = ['a','b','c','d','e','f','g','h','j','k','l','m','n','o','p','q','r','s','t']
        return (self.list.index(hand[0]), int(hand[1:])-1)

    def _next_turn(self, coord, new_state):
        self.turn += 1
        #self.previous_move = coord
        self.board = new_state
        if new_state.current_player == 'w':
            new_state.current_player = 'b'
        else:
            new_state.current_player = 'w'

    def play_at(self, state, coord):
        if self.is_legal(state, coord):
            new_state = state.move(coord, state.current_player)
            self._next_turn(coord, new_state)
            self.board = new_state
            return new_state
        else:
            raise RuntimeError

    def next_state(self, coord, state):
        # TODO doesn't place the right color && doesn't capture
        next_goban = self.board.move(coord, state.current_player)
        return next_goban

    def is_legal(self, state, coord):
        new_state = state.clone()
        new_state = new_state.move(coord, new_state.current_player)
        return (state.goban[coord[1]][coord[0]] == "0" and not new_state.is_suicide(coord, new_state.current_player))

    def winner(self, state):
        w_pts = state.territory('w') + state.captured_pieces['w'] + self.komi
        b_pts = state.territory('b') + state.captured_pieces['b']
        if w_pts > b_pts:
            return 'w'
        elif w_pts < b_pts:
            return 'b'
        
    def is_legal_fn(self):
        def legal(move):
            return self.is_legal(self.board, move)
        return legal
    
    def legal_moves(self, state):
        return list(filter(self.is_legal_fn(), state.all_coords()))

    def play(self, state, move):
        self.play_at(state, move)

    def is_over(self, state):
        return len(self.legal_moves(state)) <= 5



