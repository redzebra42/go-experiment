import copy
import random
from MCT import *

def init_board(board):
    "initialize the board to the starting position"
    board[3][3], board[4][4], board[3][4], board[4][3] = 1, 1, 2, 2

class Oboard():

    def __init__(self, board=None, player=2, size=8, prev_move=None) -> None:
        self.board = copy.deepcopy(board)        #(0: empty, 1: white, 2: black, 3: legal move)
        if self.board == None:
            self.board = [[0 for i in range(8)] for j in range(8)]
            init_board(self.board)
        self.current_player = player
        self.size = size
        self.prev_move = prev_move
        self.two_previous_moves = [self.prev_move]
        self.legal_moves()

    def curr_player(self):
        return self.current_player
    
    def clone(self):
        new_child = Oboard(self.board, self.current_player, self.size, self.prev_move)
        return new_child

    def int_to_player(self, n):
        if n == 0:
            return " "
        elif n == 1:
            return "O"
        elif n == 2:
            return "#"
        elif n == 3:
            return "."
        else:
            raise RuntimeError("n should be 0, 1 or 2")

    def print_board(self):
        print("  a b c d e f g h")
        for i in range(len(self.board)):
            print(i + 1, ("|".join(self.int_to_player(self.board[i][j]) for j in range(len(self.board)))))
    
    def neighbours(self, coord):
        '''Returns an array of neighbouring coordinates, of length 2 to 4.'''
        if coord[0] == 0:
            if coord[1] == 0:
                return [(0,1), (1,0)]
            elif coord[1] == self.size - 1:
                return [(0,self.size - 2), (1,self.size - 1)]
            else:
                return [(0, coord[1]-1),
                        (0, coord[1]+1),
                        (1, coord[1])]
        elif coord[0] == self.size - 1:
            if coord[1] == 0:
                return [(self.size - 1, 1), (self.size - 2, 0)]
            elif coord[1] == self.size - 1:
                return [(self.size - 1, self.size - 2), (self.size - 2, self.size - 1)]
            else:
                return [(self.size - 1, coord[1]-1),
                        (self.size - 1, coord[1]+1),
                        (self.size - 2, coord[1])]
        else:
            if coord[1] == 0:
                return [(coord[0]-1, 0), (coord[0]+1, 0), (coord[0], 1)]
            elif coord[1] == self.size - 1:
                return [(coord[0]-1, self.size - 1), (coord[0]+1, self.size - 1), (coord[0], self.size - 2)]
            else:
                return [(coord[0]-1, coord[1]),
                        (coord[0]+1, coord[1]),
                        (coord[0], coord[1]-1),
                        (coord[0], coord[1]+1)]
            
    def occupied_tiles(self):
        """retunrs dictionnary with 1: [list of white coords], 2: [list of black coords]"""
        occ_tiles = {1: [], 2: []}
        for i in range(self.size):
            for j in range(self.size):
                if self.board[i][j] == 1:
                    occ_tiles[1].append((i,j))
                elif self.board[i][j] == 2:
                    occ_tiles[2].append((i,j))
        return occ_tiles
    
    def opp_player(self):
        if self.current_player == 1:
            return 2
        else:
            return 1

    def is_legal_dir(self, move):
        if move == (4, 6):  #debug
            move = (4, 6)
        if self.board[move[0]][move[1]] in (0, 3):
            if move[0] < self.size - 1:
                i = move[0] + 1
                while i < self.size - 1 and self.board[i][move[1]] == self.opp_player():
                    i += 1
                if (i != move[0] + 1) and (self.board[i][move[1]] == self.current_player):
                    return (True, 'U')
            if move[0] > 0:
                i = move[0] - 1
                while i > 0 and self.board[i][move[1]] == self.opp_player():
                    i -= 1
                if (i != move[0] - 1) and (self.board[i][move[1]] == self.current_player):
                    return (True, 'D')
            if move[1] < self.size - 1:
                j = move[1] + 1
                while j < self.size - 1 and self.board[move[0]][j] == self.opp_player():
                    j += 1
                if (j != move[1] + 1) and (self.board[move[0]][j] == self.current_player):
                    return (True, 'R')
            if move[1] > 0:
                j = move[1] - 1
                while j > 0 and self.board[move[0]][j] == self.opp_player():
                    j -= 1
                if (j != move[1] - 1) and (self.board[move[0]][j] == self.current_player):
                    return (True, 'L')
            if move[0] < self.size - 1 and move[1] < self.size - 1:
                i,j = move[0] + 1, move[1] + 1
                while i < self.size - 1 and j < self.size - 1 and self.board[i][j] == self.opp_player():
                    i += 1
                    j += 1
                if (i != move[0] + 1) and (self.board[i][j] == self.current_player):
                    return (True, 'DR')
            if move[0] < self.size - 1 and move[1] > 0:
                i,j = move[0] + 1, move[1] - 1
                while i < self.size - 1 and j > 0 and self.board[i][j] == self.opp_player():
                    i += 1
                    j -= 1
                if (i != move[0] + 1) and (self.board[i][j] == self.current_player):
                    return (True, 'DL')
            if move[0] > 0 and move[1] > 0:
                i,j = move[0] - 1, move[1] - 1
                while i > 0 and  j > 0 and self.board[i][j] == self.opp_player():
                    i -= 1
                    j -= 1
                if (i != move[0] - 1) and (self.board[i][j] == self.current_player):
                    return (True, 'UL')
            if move[0] > 0 and move[1] < self.size - 1:
                i,j = move[0] - 1, move[1] + 1
                while i > 0 and j < self.size - 1 and self.board[i][j] == self.opp_player():
                    i -= 1
                    j += 1
                if (i != move[0] - 1) and (self.board[i][j] == self.current_player):
                    return (True, 'UR')
            return (False, None)
        else:
            return (False, None)
    
    def is_legal(self, move):
        return self.is_legal_dir(move)[0]
    
    def reverse(self, move, dir):
        if dir == 'R':
            i = move[1] + 1
            while self.board[move[0]][i] == self.opp_player():
                self.board[move[0]][i] = self.current_player
                i += 1
        elif dir == 'L':
            i = move[1] - 1
            while self.board[move[0]][i] == self.opp_player():
                self.board[move[0]][i] = self.current_player
                i -= 1
        elif dir == 'U':
            i = move[0] + 1
            while self.board[i][move[1]] == self.opp_player():
                self.board[i][move[1]] = self.current_player
                i += 1
        elif dir == 'D':
            i = move[0] - 1
            while self.board[i][move[1]] == self.opp_player():
                self.board[i][move[1]] = self.current_player
                i -= 1
        elif dir == 'DR':
            i = move[0] + 1
            j = move[1] + 1
            while self.board[i][j] == self.opp_player():
                self.board[i][j] = self.current_player
                i += 1
                j += 1
        elif dir == 'UR':
            i = move[0] - 1
            j = move[1] + 1
            while self.board[i][j] == self.opp_player():
                self.board[i][j] = self.current_player
                i -= 1
                j += 1
        elif dir == 'DL':
            i = move[0] + 1
            j = move[1] - 1
            while self.board[i][j] == self.opp_player():
                self.board[i][j] = self.current_player
                i += 1
                j -= 1
        elif dir == 'UL':
            i = move[0] - 1
            j = move[1] - 1
            while self.board[i][j] == self.opp_player():
                self.board[i][j] = self.current_player
                i -= 1
                j -= 1 
    
    def legal_moves(self):
        leg_moves = []
        for i in range(self.size):
            for j in range(self.size):
                move = (i, j)
                if self.is_legal(move):
                    self.board[move[0]][move[1]] = 3
                    leg_moves.append(move)
                elif self.board[move[0]][move[1]] == 3:
                    self.board[move[0]][move[1]] = 0
        leg_moves.append('pass')
        return leg_moves
    
    def is_over(self):
        if len(self.legal_moves()) == 1:
            new_state = self.clone()
            new_state.play_at('pass')
            if len(new_state.legal_moves()) == 1:
                return True
        return False
    
    def score(self):
        b = 0
        w = 0
        for line in self.board:
            for stone in line:
                if stone == 1:
                    w += 1
                elif stone == 2:
                    b += 1
        return w - b
    
    def winner(self):
        '''return 1 for white, 2 for black, 0 for equal scores'''
        if self.is_over():
            score = self.score()
            if score > 0:
                return 1
            elif score < 0:
                return 2
            else:
                return 0
            
    def play_random(self):
        leg_moves = self.legal_moves()
        i = random.randint(0, len(leg_moves) - 1)
        self.play_at(leg_moves[i])

    def rand_simulation(self):
        while not self.is_over():
            self.play_random()

    def play_at(self, move):
        if move == 'pass':
            self.current_player = self.opp_player()
            self.prev_move = move
            self.legal_moves()
        else:
            legal_dir = self.is_legal_dir(move)
            if legal_dir[0]:
                self.reverse(move, legal_dir[1])
                self.board[move[0]][move[1]] = self.current_player
                self.current_player = self.opp_player()
                self.prev_move = move
                self.legal_moves()
            else:
                print("illegal move")
    
    def play_at_and_print(self, move):
        self.play_at(move)
        self.print_board()
    
class Ogame():

    def __init__(self) -> None:
        self.state = Oboard()

        '''
        game class that has the following functions:
        X legal_moves(state) 
        X play_at(state, move)
        X is_over(state)
        X winner(state)
        X rand_simulation(state)
        X play_mct()
        state class with the following funcyions:
        X curr_player()
        X clone()
        '''
    
    def txt_move_to_coord(self, move):
        if move == 'pass':
            return move
        '''Convert a textual hand like c12 into coordinates like (2, 12).'''
        L = ['a','b','c','d','e','f','g','h']
        return (int(move[1:])-1, L.index(move[0]))
    
    def legal_moves(self, state):
        return state.legal_moves()
    
    def play_at(self, state, move):
        state.play_at(move)

    def is_over(self, state):
        return state.is_over()

    def winner(self, state):
        return state.winner()

    def rand_simulation(self, state):
        state.rand_simulation()
        return state

    def play_mct(self, state, coord, player):
        res = Oboard(state.board, player, state.size, state.prev_move)
        res.play_at(coord)
        return res
    
    def _mct_move(self, state, move):
        new_state = state.clone()
        new_state.curr_player = new_state.opp_player()
        new_state.prev_move = move
        new_state.legal_moves()


def is_legal_test(board1):
    legal_board = [[None for i in range(board1.size)] for j in range(board1.size)]
    for i in range(board1.size):
        for j in range(board1.size):
            legal_board[i][j] = board1.is_legal((i, j))
    for i in range(len(legal_board)):
        for j in range(len(legal_board)):
            if legal_board[i][j]:
                board1.board[i][j] = 3


if __name__ == "__main__":
    game = Ogame()
    state = game.state
    mct = MCT(game, state)

    def play_at(coord, state=state):
        if state.is_legal(coord):
            game.play_at(state, coord)
            state.print_board()
            mct.set_played_move(coord)
        else:
            print("illegal move")

    def tree_search(search_depth):
        mct.new_move(search_depth)
        #state = mct.root.state
        state.print_board()

    mct.root.state.print_board()


    while True:

        move = input(str('next move: '))

        if move == None:
            continue

        coord = game.txt_move_to_coord(move)
        play_at(coord)
        tree_search(100)

