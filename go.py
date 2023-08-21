import board
import random
import time

class Go():


    def __init__(self):
        self.board = board.Board()
        self.current_player = 'w'
        self.turn = 0
        self.komi = 3.5
        self.is_chinese_rule_set = True

    def hand_to_coord(self, hand):
        '''Convert a textual hand like c12 into coordinates like (2, 12).'''
        self.list = ['a','b','c','d','e','f','g','h','j','k','l','m','n','o','p','q','r','s','t']
        return (self.list.index(hand[0]), int(hand[1:])-1)

    def _next_turn(self, new_state, move):
        new_state.two_previous_moves[1] = new_state.two_previous_moves[0]
        new_state.two_previous_moves[0] = move
        self.turn += 1
        if new_state.current_player == 'w':
            new_state.current_player = 'b'
        else:
            new_state.current_player = 'w'

    def play_at(self, state, coord):
        clock = time.clock_gettime(0)
        if coord == 'pass':
            new_state = state.clone()
            self._next_turn(new_state, coord)
            #print("play_at: ", time.clock_gettime(0) - clock)
            return new_state
        else:
            if self.is_legal(state, coord):
                new_state = state.move(coord, state.current_player)
                self._next_turn(new_state, coord)
                #print("play_at: ", time.clock_gettime(0) - clock)
                return new_state
            else:
                raise RuntimeError
    
    def _mct_move(self, state, move):
        new_state = state.clone()
        self._next_turn(new_state, move)
    
    def play_pass(self):
        self._next_turn(self.board, 'pass')

    def next_state(self, coord, state):
        next_goban = self.board.move(coord, state.current_player)
        return next_goban

    def is_legal(self, state, coord):
        if coord == 'pass' or type(coord) == str:
            return True
        else:
            return state.current_player in state.leg_move_board[coord[1]][coord[0]]

    def winner(self, state):
        w_pts = state.territory('w') + state.captured_pieces['w'] + self.komi
        b_pts = state.territory('b') + state.captured_pieces['b']
        if self.is_chinese_rule_set:
            for line in state.goban:
                for piece in line:
                    if piece == 'w':
                        w_pts += 1
                    elif piece == 'b':
                        b_pts += 1
        if w_pts > b_pts:
            return 'w'
        elif w_pts < b_pts:
            return 'b'
        
    def is_legal_fn(self, state):
        def legal(move):
            return self.is_legal(state, move)
        return legal
    
    def legal_moves(self, state):
        clock = time.clock_gettime(0)
        leg_moves = []
        for i in range(state.size):
            for j in range(state.size):
                if state.current_player in state.leg_move_board[i][j]:
                    leg_moves.append((i, j))
        leg_moves.append('pass')
        #print("legal moves: ", time.clock_gettime(0) - clock)
        return leg_moves

    def is_over(self, state):
        return state.two_previous_moves == ['pass', 'pass']
    
    def play_random(self, state):
        clock = time.clock_gettime(0)
        leg_moves = self.legal_moves(state)
        k = random.randint(0, len(leg_moves)-1)
        coord = leg_moves[k]
        if coord != 'pass':
            #print("play random: ", time.clock_gettime(0) - clock)
            return self.play_at(state, (coord[1], coord[0]))
        else:
            #print("play random: ", time.clock_gettime(0) - clock)
            return self.play_at(state, coord)
    
    def rand_simulation(self, state):
        '''returns the new_state of the game after a randomly played game'''
        new_state = state.clone()
        i = 0
        while not self.is_over(new_state) and i < 500:
            new_state = self.play_random(new_state)
            i += 1
        print(i)
        return new_state
    
