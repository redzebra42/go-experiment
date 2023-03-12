import board

class Go():


    def __init__(self):
        self.board = board.Board()
        self.current_player = 'w'
        self.opp_player = 'b' if self.current_player == 'w' else 'w'
        self.group_list = []
        

    def hand_to_coord(self,hand):
        '''Convert a textual hand like c12 into coordinates like (2, 12).'''
        self.list = ['a','b','c','d','e','f','g','h','j','k','l','m','n','o','p','q','r','s','t']
        return (self.list.index(hand[0]), int(hand[1:])-1)

    def move(self, coord):
        self.board.goban[coord[1]][coord[0]] = self.current_player

    def next_turn(self):
        if self.current_player == 'w':
            self.current_player = 'b'
        else:
            self.current_player = 'w'

    
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
            
    def group(self, coord, goban):
        neighbours = self.neighbours(coord)
        self.group_list.append(coord)
        for neighb in neighbours:
            if goban[neighb[1]][neighb[0]] != goban[coord[1]][coord[0]]:
                break
            else:
                self.group(neighb, self.board.goban)
        return self.group_list


    def capture (self, coord):
        if self.neighbours(coord) != ['0','0','0','0']:
            return True
