from tkinter import *
#from tkinter import ttk
import copy
import starting_state as st
import time
from numpy import log

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






#TODO représenter un plateau par un nombre binaire (dans l'ordre de lecture du plateau)
#ou chaque case est 00 pour vide, 01 pour blanc 10 pour noir et 11 pour oeuil par exemple (pour éviter de jouer dans les yeux).
#permetterai peut être d'éviter les doublons dans l'arbre... (si on retrouve une configuration dèja rencontrée, faire qqchose)
#capture et tout ça peut peut être se trouver en faisant des opérations sur les bits, mait jsp si c'est faisable en python







class Board():

    '''
    Board state, print board
    has all the information needed to play from here (board, captures)
    '''

    def __init__(self, goban=st.goban, captured_pieces=st.caps, curr_player=st.player ,two_previous_moves=st.two_prev_moves, size=st.size, leg_move_board=None, is_chinese_rule_set=True, komi=3.5, groups=None):
        self.size = size
        self.current_player = curr_player
        self.goban = copy.deepcopy(goban)
        self.captured_pieces =  copy.copy(captured_pieces)
        self.two_previous_moves = copy.deepcopy(two_previous_moves)
        self.leg_move_board = copy.deepcopy(leg_move_board)
        self.is_chinese_rule_set = is_chinese_rule_set
        self.komi = komi
        if leg_move_board == None:
            self.leg_move_board = self.initiate_legal_moves()
        else:
            self.leg_move_board = copy.deepcopy(leg_move_board)

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
            
    
    def rgb_hack(self, rgb):
        return "#%02x%02x%02x" % rgb  

    def print_tile_canvas(self, coord, cnvs):
        i,j = coord[0], coord[1]
        #grp = self.groups[j][i]
        if self.goban[j][i] == "b":
            cnvs.create_oval(43+35*i,43+35*j,77+35*i,77+35*j, fill="black")
        elif self.goban[j][i] == "w":
            cnvs.create_oval(43+35*i,43+35*j,77+35*i,77+35*j, fill="white", outline="white")
        else:
            #pass
            bias = (int(100 * (self.inside_terr_bias(self.current_player, (i, j)) + self.capture_bias(self.current_player, (i, j)))))
            cnvs.create_oval(53+35*i,53+35*j,67+35*i,67+35*j, fill= self.rgb_hack((bias, bias, bias)))
        #cnvs.create_oval(53+35*i,53+35*j,67+35*i,67+35*j, fill= self.rgb_hack(((50 + 40*grp)%255, (130 + 170*grp)% 255, (80*grp)% 255)))

    def print_tkinter_board(self, cnvs):
        size = self.size
        move = self.two_previous_moves[0]
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
        if move != None:
            if move != 'pass':
                y, x = 60+35*move[1], 60+35*move[0]
                cnvs.create_oval(x-4, y-4, x+4, y+4, fill="red")

    def _group_rec(self, coord, group_list:list):
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
        self.goban[coord[1]][coord[0]] = player
        captures = self.capture(coord, self.opposite(player))
        self.captured_pieces[player] += captures
        self.update_legal_moves(coord, player, captures)       #TODO c'est cette fonction qui prend du temps (et que celle là)

    def opposite(self, player):
        if player == 'w':
            return 'b'
        elif player == 'b':
            return 'w'
        else:
            raise RuntimeError('Illegal argument, player should be "b" or "w"')

    def move(self, coord, player):
        result = Board(self.goban, self.captured_pieces, player, self.two_previous_moves, self.size, self.leg_move_board)
        if type(coord) != str:
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
        #clock = time.clock_gettime(0)
        points = 0
        already_counted = []
        for i in range(len(self.goban)):
            for j in range(len(self.goban[0])):
                    coord = (j,i)
                    coord_group = self.group(coord)
                    if self.goban[i][j] == "0" and not(coord in already_counted) and all(self.goban[x[1]][x[0]] == color for x in self.group_neighbours(coord_group)):
                        points += len(coord_group)
                    if not(coord in already_counted):
                        for k in range(len(coord_group)):
                            already_counted.append(coord_group[k])
        #print("territory: ", time.clock_gettime(0) - clock)
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
        clock = time.clock_gettime(0)
        if self.goban[coord[1]][coord[0]] == '0':
            res = 0
            neighbours = self.neighbours(coord)
            for neighb in neighbours:
                if self.goban[neighb[1]][neighb[0]] == '0':
                    break
                else:
                    group = self.group(neighb)
                    if self.goban[neighb[1]][neighb[0]] == self.opposite(player) and self.liberty(group)[0] > 1:
                        res += 1
                    elif self.goban[neighb[1]][neighb[0]] == player and self.liberty(group)[0] == 1:
                        res += 1
            #print("is_legal: ", time.clock_gettime(0) - clock)
            return res != len(neighbours)
        else:
            #print("is_legal: ", time.clock_gettime(0) - clock)
            return False
    
    def update_legal_moves(self, move, curr_player, captures):
        '''
        Updates the legal_move_board
        could be optimized by not checking multiple times the same group in the neighb loop
        '''
        clock = time.clock_gettime(0)
        if move != 'pass':
            self.leg_move_board[move[1]][move[0]] = []
            self.leg_move_board = self.initiate_legal_moves()
        #print("update legal moves: ", time.clock_gettime(0) - clock)

    def initiate_legal_moves(self):
        clock = time.clock_gettime(0)
        leg_move_board = [[[] for i in range(self.size)] for j in range(self.size)]
        for coord in self.all_coords():
            if self.goban[coord[1]][coord[0]] == '0':
                if self.is_legal(coord, 'w'):
                    leg_move_board[coord[1]][coord[0]].append('w')
                if self.is_legal(coord, 'b'):
                    leg_move_board[coord[1]][coord[0]].append('b')
        #print("initiate legal moves: ", time.clock_gettime(0) - clock)
        return leg_move_board
    
    def winner(self):
        w_pts = self.territory('w') + self.captured_pieces['w'] + self.komi
        b_pts = self.territory('b') + self.captured_pieces['b']
        if self.is_chinese_rule_set:
            for line in self.goban:
                for piece in line:
                    if piece == 'w':
                        w_pts += 1
                    elif piece == 'b':
                        b_pts += 1
        if w_pts > b_pts:
            return 'w'
        elif w_pts < b_pts:
            return 'b'
    
    def is_over(self):
        return self.two_previous_moves == ['pass', 'pass']
    
    def legal_moves(self):
        leg_moves = []
        for i in range(self.size):
            for j in range(self.size):
                if self.current_player in self.leg_move_board[i][j]:
                    leg_moves.append((j, i))
        leg_moves.append('pass')
        return leg_moves

    def inside_terr_bias(self, player, move):
        move_group = self.group(move)
        neighb_group = self.group_neighbours(move_group)
        coord = neighb_group[0]
        if self.goban[coord[1]][coord[0]] == player:
            return 1 / 2*log(len(move_group) + 1)
        else:
            return 0

    def capture_bias(self, player, move):
        #TODO améliorer l'efficacité si je l'utilise dans le MCT (pas faire une copie + capture, un peu comme is_legal)
        test_board = self.clone()
        return log(1 + test_board.capture(move, self.opposite(player)))

    def __str__(self) -> str:
        res = ''
        for i in range(self.size):
            res += str(f'{self.goban[i]}\n')
        return res