import board
import copy

class Go():


    def __init__(self):
        self.board = board.Board()
        self.current_player = 'b'
        self.turn = 0
        self.captured_pieces = []
        self.previous_move = None
        self.states = []

    def hand_to_coord(self, hand):
        '''Convert a textual hand like c12 into coordinates like (2, 12).'''
        self.list = ['a','b','c','d','e','f','g','h','j','k','l','m','n','o','p','q','r','s','t']
        return (self.list.index(hand[0]), int(hand[1:])-1)

    def _next_turn(self, coord, new_state):
        self.turn += 1
        self.previous_move = coord
        self.states.append(new_state.goban)
        self.board = new_state
        if self.current_player == 'w':
            self.current_player = 'b'
        else:
            self.current_player = 'w'

    def play_at(self, coord):
        if self.is_legal(coord):
            new_state = self.board.move(coord, self.current_player)
            self._next_turn(coord, new_state)
            return True
        else:
            return False

    def is_ko(self, goban):
        '''tests if there is a ko position only for the two_last_sates''' 
        return len(self.states) > 2 and goban in self.states

    def next_state(self, coord):
        # TODO doesn't place the right color && doesn't
        next_goban = self.board.move(coord, self.current_player)
        return next_goban

    def is_legal(self, coord):
        return (self.board.goban[coord[1]][coord[0]] == "0" and (not self.is_ko(self.board.move(coord, self.current_player).goban)))


