import board

class Go():


    def __init__(self):
        self.board = board.Board()
        self.current_player = 'w'
        self.opp_player = 'b'
        self.group_list = []
        self.turn = 0
        self.captured_pieces = []
        

    def hand_to_coord(self,hand):
        '''Convert a textual hand like c12 into coordinates like (2, 12).'''
        self.list = ['a','b','c','d','e','f','g','h','j','k','l','m','n','o','p','q','r','s','t']
        return (self.list.index(hand[0]), int(hand[1:])-1)

    def move(self, coord):
        if self.board.goban[coord[1]][coord[0]] in ['0','x']:
            self.board.goban[coord[1]][coord[0]] = self.current_player

    def next_turn(self):
        self.turn += 1
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
            
            
    def group_rec(self, coord, goban):                #recursive fonction for groups (doesn't work yet, or does it ?)
        neighbours = self.neighbours(coord)
        self.group_list.append(coord)
        for neighb in neighbours:
            if (not(neighb in self.group_list)) and goban[neighb[1]][neighb[0]] == goban[coord[1]][coord[0]]:
                self.group_rec(neighb, goban)
        return
            
    def group(self, coord, goban):
        self.group_list = []
        self.group_rec(coord, goban)
        return self.group_list
    
    def liberty(self, group, goban):
        lib_coords = []
        liberties = 0
        for coord in group:
            for neighb in self.neighbours(coord):
                if (not (neighb in lib_coords)) and goban[neighb[1]][neighb[0]] in ["0","x"]:
                    lib_coords.append(neighb)
                    liberties += 1
        return liberties


    def capture (self, new_coord):
        '''tests if there is a capture for a new move and captures the stones'''
        goban = self.board.goban
        for neighb in self.neighbours(new_coord):
            if goban[neighb[1]][neighb[0]] == self.opp_player and self.liberty(self.group(neighb, goban), goban) == 0:
                for coord in self.group(neighb, goban):
                    self.captured_pieces.append(self.opp_player)
                    goban[coord[1]][coord[0]] = '0'
    


