import board
import copy

class Go():


    def __init__(self):
        self.board = board.Board()
        self.current_player = 'b'
        self.opp_player = 'w'
        self.group_list = []
        self.turn = 0
        self.captured_pieces = []
        self.previous_move = None
        self.states = []
        

    def hand_to_coord(self,hand):
        '''Convert a textual hand like c12 into coordinates like (2, 12).'''
        self.list = ['a','b','c','d','e','f','g','h','j','k','l','m','n','o','p','q','r','s','t']
        return (self.list.index(hand[0]), int(hand[1:])-1)

    def move(self, coord):
        self.board.goban[coord[1]][coord[0]] = self.current_player

    def next_turn(self,coord):
        self.turn += 1
        self.previous_move = coord
        self.states.append(copy.deepcopy(self.board.goban))
        if self.current_player == 'w':
            self.current_player = 'b'
            self.opp_player = 'w'
        else:
            self.current_player = 'w'
            self.opp_player = 'b'

    
    def neighbours(self, coord):
        '''Returns an array of neighbouring coordinates, of length 2 to 4.'''
        if coord[0] == 0:
            if coord[1] == 0:
                return [(0,1), (1,0)]
            elif coord[1] == 18:
                return [(0,17), (1,18)]
            else:
                return [(0, coord[1]-1),
                        (0, coord[1]+1),
                        (1, coord[1])]
        elif coord[0] == 18:
            if coord[1] == 0:
                return [(18, 1), (17, 0)]
            elif coord[1] == 18:
                return [(18, 17), (17, 18)]
            else:
                return [(18, coord[1]-1),
                        (18, coord[1]+1),
                        (17, coord[1])]
        else:
            if coord[1] == 0:
                return [(coord[0]-1, 0), (coord[0]+1, 0), (coord[0], 1)]
            elif coord[1] == 18:
                return [(coord[0]-1, 18), (coord[0]+1, 18), (coord[0], 17)]
            else:
                return [(coord[0]-1, coord[1]),
                        (coord[0]+1, coord[1]),
                        (coord[0], coord[1]-1),
                        (coord[0], coord[1]+1)]
            
            
    def _group_rec(self, coord):
        goban = self.board.goban
        neighbours = self.neighbours(coord)
        self.group_list.append(coord)
        for neighb in neighbours:
            if (not(neighb in self.group_list)) and goban[neighb[1]][neighb[0]] == goban[coord[1]][coord[0]]:
                self._group_rec(neighb)
        return
            
    def group(self, coord):
        self.group_list = []
        self._group_rec(coord)
        return self.group_list
    
    def liberty(self, group):
        '''returns a tuple (number of liberties, list of all liberties)'''
        goban = self.board.goban
        lib_coords = []
        liberties = 0
        for coord in group:
            for neighb in self.neighbours(coord):
                if (not (neighb in lib_coords)) and goban[neighb[1]][neighb[0]] in ["0","x"]:
                    lib_coords.append(neighb)
                    liberties += 1
        return (liberties, lib_coords)
    
    def group_neighbours(self, group):
        '''returns list of coordinates of neighbours of a group'''
        goban = self.board.goban
        neighb_coords = []
        for coord in group:
            for neighb in self.neighbours(coord):
                if (not (neighb in neighb_coords)) and goban[neighb[1]][neighb[0]] != goban[coord[1]][coord[0]]:
                    neighb_coords.append(neighb)
        return neighb_coords


    def capture (self, new_coord):
        '''tests if there is a capture for a new move and captures the stones'''
        goban = self.board.goban
        for neighb in self.neighbours(new_coord):
            if goban[neighb[1]][neighb[0]] == self.opp_player and self.liberty(self.group(neighb))[0] == 0:
                for coord in self.group(neighb):
                    self.captured_pieces.append(self.opp_player)
                    goban[coord[1]][coord[0]] = '0'
    
    
    def is_ko(self, goban):
        '''tests if there is a ko position only for the two_last_sates''' 
        return len(self.states) > 2 and goban in self.states

    def territory(self, color):
        points = 0
        already_counted = []
        for i in range(len(self.board.goban)):
            for j in range(len(self.board.goban[0])):
                    coord = (j,i)
                    if self.board.goban[i][j] == "0" and not(coord in already_counted) and all(self.board.goban[x[1]][x[0]] == color for x in self.group_neighbours(self.group(coord))):
                        points += len(self.group(coord))
                    if not(coord in already_counted):
                        for k in range(len(self.group(coord))):
                            already_counted.append(self.group(coord)[k])
        return points
    
    def next_state(self, coord):
        # TODO doesn't place the right color && doesn't
        next_goban = copy.deepcopy(self.board.goban)
        next_goban[coord[1]][coord[0]] = self.current_player
        return next_goban

    
    def is_legal(self, coord):
        return (self.board.goban[coord[1]][coord[0]] == "0" and (not self.is_ko(self.next_state(coord))))


