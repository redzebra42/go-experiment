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
            self._next_turn(state, coord)
            #print("play_at: ", time.clock_gettime(0) - clock)
        else:
            if self.is_legal(state, coord):
                state.play_at(coord, state.current_player)
                self._next_turn(state, coord)
                #print("play_at: ", time.clock_gettime(0) - clock)
            else:
                raise RuntimeError
            
    def play_mct(self, state, coord, player):
        new_state = state.move(coord, player)
        self._next_turn(new_state, coord)
        return new_state
    
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
    
    def play_random(self, state):
        clock = time.clock_gettime(0)
        leg_moves = state.legal_moves()
        k = random.randint(0, len(leg_moves)-1)
        coord = leg_moves[k]
        self.play_at(state, coord)
    
    def rand_simulation(self, state):
        '''returns the new_state of the game after a randomly played game'''
        #new_state = state.clone()
        i = 0
        while not state.is_over() and i < 500:
            self.play_random(state)
            i += 1
        #print(i)
        if i > 60:
            pass
        return state
    
