from tkinter import *
#from tkinter import ttk
import copy
import starting_state as st

starting_board_1 = [['0' for i in range(st.size)] for j in range(st.size)]
starting_board_2 = [['w', 'w', 'w', 'b', 'b', 'w', 'b', 'b', '0'],
['0', '0', 'w', 'b', 'b', 'w', 'w', 'w', 'w'],
['0', 'w', 'w', 'b', '0', 'b', 'b', 'b', 'b'],
['0', 'w', 'w', 'w', 'b', 'b', 'w', 'w', 'w'],
['0', '0', '0', 'w', 'b', 'w', 'w', 'b', '0'],
['0', '0', 'w', 'b', 'b', 'w', '0', 'w', 'b'],
['0', '0', 'w', 'b', 'w', 'w', '0', 'w', 'w'],
['0', '0', 'w', 'w', 'w', 'w', '0', '0', 'w'],
['w', 'w', 'w', 'w', 'w', '0', '0', 'w', '0']]

class Board():

    '''
    Board state, print board
    has all the information needed to play from here (board, captures)
    '''

    def __init__(self, goban=st.goban, captured_pieces=st.caps, curr_player=st.player ,two_previous_moves=st.two_prev_moves, size=st.size):
        self.size = size
        self.current_player = curr_player
        self.goban = copy.deepcopy(goban)
        self.captured_pieces =  copy.copy(captured_pieces)
        self.two_previous_moves = copy.deepcopy(two_previous_moves)
        self.leg_move_board = [[[] for i in range(self.size)] for j in range(self.size)]
        self.initiate_legal_moves()

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
   
    def goban_to_print(self, tile):
        if tile == '0':
            return '|  '
        elif tile == 'b':
            return '| 0'
        elif tile == 'w':
            return '| O'
        elif tile == 'x':
            return '| x'
        
    def print_board(self):
        print("  A  B  C  D  E  F  G  H  J  K  L  M  N  O  P  Q  R  S  T")
        for i in range(len(self.goban)):
            print("".join([self.goban_to_print(self.goban[i][j]) for j in range(len(self.goban[0]))]), str(i+1))

    def print_tile_canvas(self, coord, cnvs):
        i,j = coord[0], coord[1]
        if self.goban[j][i] == "b":
            cnvs.create_oval(43+35*i,43+35*j,77+35*i,77+35*j, fill="black")
        elif self.goban[j][i] == "w":
            cnvs.create_oval(43+35*i,43+35*j,77+35*i,77+35*j, fill="white", outline="white")

    def print_tkinter_board(self, cnvs,):
        size = self.size
        cnvs.pack(side=LEFT)
        cnvs.create_rectangle(40, 40, 80+35*(size-1), 80+35*(size-1), width=3, fill="orange", outline="orange")
        cnvs.create_rectangle(60, 60, 60+35*(size-1), 60+35*(size-1), width=3)
        for i in range(1,size):
            cnvs.create_line(60+35*i, 60, 60+35*i, 60+35*(size-1), width=2)
        for j in range(1,size):
            cnvs.create_line(60, 60+35*j, 60+35*(size-1), 60+35*j, width=2)
        if size == 19:
            for i in [165, 375, 585]:
                for j in [165, 375, 585]:
                    cnvs.create_oval(i-5,j-5,i+5,j+5, fill="black")
        elif size == 9:
            for i in [130, 270]:
                for j in [130, 270]:
                    cnvs.create_oval(i-5,j-5,i+5,j+5, fill="black")
        for i in range(len(self.goban)):
            for j in range(len(self.goban[0])):
                self.print_tile_canvas((i,j), cnvs)

    def _group_rec(self, coord, group_list):
        neighbours = self.neighbours(coord)
        group_list.append(coord)
        for neighb in neighbours:
            if (not(neighb in group_list)) and self.goban[neighb[1]][neighb[0]] == self.goban[coord[1]][coord[0]]:
                self._group_rec(neighb, group_list)
        return

    def group(self, coord):
        group_list = []
        self._group_rec(coord, group_list)
        return group_list

    def liberty(self, group):
        '''returns a tuple (number of liberties, list of all liberties)'''
        lib_coords = []
        liberties = 0
        for coord in group:
            for neighb in self.neighbours(coord):
                if (not (neighb in lib_coords)) and self.goban[neighb[1]][neighb[0]] in ["0","x"]:
                    lib_coords.append(neighb)
                    liberties += 1
        return (liberties, lib_coords)

    def play_at(self, coord, player):
        self.move(coord, player)

    def opposite(self, player):
        if player == 'w':
            return 'b'
        elif player == 'b':
            return 'w'
        else:
            raise RuntimeError('Illegal argument, player should be "b" or "w"')

    def move(self, coord, player):
        result = Board(self.goban, self.captured_pieces, player, self.two_previous_moves, self.size)
        result.goban[coord[1]][coord[0]] = player
        captures = result.capture(coord, self.opposite(player))
        result.captured_pieces[player] += captures
        result.update_legal_moves(coord, player, captures)
        return result

    def capture(self, new_coord, opp_player):
        '''tests if there is a capture for a new move and captures the stones
        Modifies the board's goban.
        Returns the number of captured pieces, 0 if nothing is captured.'''
        result = 0
        goban = self.goban
        for neighb in self.neighbours(new_coord):
            neighb_group = self.group(neighb)
            if goban[neighb[1]][neighb[0]] == opp_player and self.liberty(neighb_group)[0] == 0:
                for coord in neighb_group:
                    result += 1
                    goban[coord[1]][coord[0]] = '0'
        return result

    def group_neighbours(self, group):
        '''returns list of coordinates of neighbours of a group'''
        neighb_coords = []
        for coord in group:
            for neighb in self.neighbours(coord):
                if (not (neighb in neighb_coords)) and self.goban[neighb[1]][neighb[0]] != self.goban[coord[1]][coord[0]]:
                    neighb_coords.append(neighb)
        return neighb_coords

    def old_is_suicide(self, coord, player):
        i = 0
        group_coord = self.group(coord)
        neighbours = self.group_neighbours(group_coord)
        for neighb in neighbours:
            if self.goban[neighb[1]][neighb[0]] == self.opposite(player):
                i += 1
            else:
                return False
        if i == len(neighbours):
            return True
        return False
    
    def is_suicide(self, coord, player):
        neighbours = self.neighbours(coord)
        i = 0
        for neighb in neighbours:
            if self.goban[neighb[1]][neighb[0]] == player:
                if self.liberty(self.group(neighb))[0] > 1:
                    return False
                else:
                    i += 1
            elif self.goban[neighb[1]][neighb[0]] == self.opposite(player):
                i += 1
        if i == len(neighbours):
            return True
        else:
            return False

    def territory(self, color):
        points = 0
        already_counted = []
        for i in range(len(self.goban)):
            for j in range(len(self.goban[0])):
                    coord = (j,i)
                    if self.goban[i][j] == "0" and not(coord in already_counted) and all(self.goban[x[1]][x[0]] == color for x in self.group_neighbours(self.group(coord))):
                        points += len(self.group(coord))
                    if not(coord in already_counted):
                        for k in range(len(self.group(coord))):
                            already_counted.append(self.group(coord)[k])
        return points
    
    def clone(self):
        new_child = Board(self.goban, self.captured_pieces, self.current_player, self.two_previous_moves, self.size)
        return new_child
    
    def curr_player(self):
        return self.current_player
    
    def all_coords(self):
        res = [(i, j) for i in range(self.size) for j in range(self.size)]
        return res

    def is_legal(self, coord, player):
        res = 0
        neighbours = self.neighbours(coord)
        for neighb in neighbours:
            if self.goban[neighb[1]][neighb[0]] == self.opposite(player) and self.liberty(self.group(neighb))[0] > 1:
                res += 1
            elif self.goban[neighb[1]][neighb[0]] == player and self.liberty(self.group(neighb))[0] == 1:
                res += 1
        return (res != len(neighbours) and self.goban[coord[1]][coord[0]] == '0')
    
    def update_legal_moves(self, move, curr_player, captures):
        self.leg_move_board[move[1]][move[0]] = []
        if captures > 0:
            self.initiate_legal_moves()
        else:
            move_lib = self.liberty(self.group(move))
            new_coord = move_lib[1][0]
            if move_lib[0] == 1:
                self.leg_move_board[new_coord[1]][new_coord[0]].remove(curr_player)
            for neighb in self.neighbours(move):
                nei_group = self.group(neighb)
                nei_lib = self.liberty(nei_group)
                if self.goban[neighb[1]][neighb[0]] == self.opposite(curr_player) and nei_lib[0] == 1:
                    new_coord = nei_lib[1][0]
                    if self.is_suicide(new_coord, self.opposite(curr_player)):
                        self.leg_move_board[new_coord[1]][new_coord[0]].remove(self.opposite(curr_player))
                elif self.goban[neighb[1]][neighb[0]] == '0':
                    if self.is_suicide(neighb, curr_player):
                        self.leg_move_board[neighb[1]][neighb[0]].remove(curr_player)
                    elif self.is_suicide(neighb, self.opposite(curr_player)):
                        self.leg_move_board[neighb[1]][neighb[0]].remove(self.opposite(curr_player))

    def initiate_legal_moves(self):
        self.leg_move_board = [[[] for i in range(self.size)] for j in range(self.size)]
        for coord in self.all_coords():
            if self.is_legal(coord, 'w'):
                self.leg_move_board[coord[1]][coord[0]].append('w')
            if self.is_legal(coord, 'b'):
                self.leg_move_board[coord[1]][coord[0]].append('b')

    def __str__(self) -> str:
        res = ''
        for i in range(self.size):
            res += str(f'{self.goban[i]}\n')
        return res