import copy

def init_board(board):
    "initialize the board to the starting position"
    board[3][3], board[4][4], board[3][4], board[4][3] = 1, 1, 2, 2

class Oboard():

    def __init__(self, board=None ) -> None:
        self.board = copy.deepcopy(board)        #(0: empty, 1: white, 2: black, 3: legal move)
        if self.board == None:
            self.board = [[0 for i in range(8)] for j in range(8)]
            init_board(self.board)
        self.current_player = 2
        self.size = 8

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
                while self.board[i][move[1]] == self.opp_player():
                    i += 1
                if (i != move[0] + 1) and (self.board[i][move[1]] == self.current_player):
                    return (True, 'U')
            if move[0] > 0:
                i = move[0] - 1
                while self.board[i][move[1]] == self.opp_player():
                    i -= 1
                if (i != move[0] - 1) and (self.board[i][move[1]] == self.current_player):
                    return (True, 'D')
            if move[1] < self.size - 1:
                j = move[1] + 1
                while self.board[move[0]][j] == self.opp_player():
                    j += 1
                if (j != move[1] + 1) and (self.board[move[0]][j] == self.current_player):
                    return (True, 'R')
            if move[1] > 0:
                j = move[1] - 1
                while self.board[move[0]][j] == self.opp_player():
                    j -= 1
                if (j != move[1] - 1) and (self.board[move[0]][j] == self.current_player):
                    return (True, 'L')
            if move[0] < self.size - 1 and move[1] < self.size - 1:
                i,j = move[0] + 1, move[1] + 1
                while self.board[i][j] == self.opp_player():
                    i += 1
                    j += 1
                if (i != move[0] + 1) and (self.board[i][j] == self.current_player):
                    return (True, 'UR')
            if move[0] < self.size - 1 and move[1] > 0:
                i,j = move[0] + 1, move[1] - 1
                while self.board[i][j] == self.opp_player():
                    i += 1
                    j -= 1
                if (i != move[0] + 1) and (self.board[i][j] == self.current_player):
                    return (True, 'UL')
            if move[0] > 0 and move[1] > 0:
                i,j = move[0] - 1, move[1] - 1
                while self.board[i][j] == self.opp_player():
                    i -= 1
                    j -= 1
                if (i != move[0] - 1) and (self.board[i][j] == self.current_player):
                    return (True, 'DL')
            if move[0] > 0 and move[1] < self.size - 1:
                i,j = move[0] - 1, move[1] + 1
                while self.board[i][j] == self.opp_player():
                    i -= 1
                    j += 1
                if (i != move[0] - 1) and (self.board[i][j] == self.current_player):
                    return (True, 'DR')
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


    def play_at(self, move):
        print(move)
        legal_dir = self.is_legal_dir(move)
        print(legal_dir[1])
        if legal_dir[0]:
            self.reverse(move, legal_dir[1])
            self.board[move[0]][move[1]] = self.current_player
            self.current_player = self.opp_player()
            self.print_board()
        else:
            print("illegal move")
    
class Ogame():

    def __init__(self) -> None:
        self.state = Oboard()
    
    def txt_move_to_coord(self, move):
        '''Convert a textual hand like c12 into coordinates like (2, 12).'''
        L = ['a','b','c','d','e','f','g','h']
        return (int(move[1:])-1, L.index(move[0]))
    
    def play_at(self, state, move):
        state.play_at(move)


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
    board = Oboard()
    game = Ogame()
    is_legal_test(board)
    board.print_board()
    print(board.occupied_tiles())


    while True:
        move = input(str('next move: '))

        if move == None:
            continue

        coord = game.txt_move_to_coord(move)
        game.play_at(board, coord)


