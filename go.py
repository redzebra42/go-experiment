import board

class Go():


    def __init__(self):
        self.board = board.Board()
        self.current_player = 'w'
        self.opp_player = 'b' if self.current_player == 'w' else 'w'
        

    def hand_to_coord(self,hand):
        '''Convert a textual hand like c12 into coordinates like (2, 12).'''
        self.list = ['a','b','c','d','e','f','g','h','j','k','l','m','n','o','p','q','r','s','t']
        return (self.list.index(hand[0]), int(hand[1:])-1)

    def move(self, coord):
        self.board.goban[coord[1]][coord[0]] = self.current_player

    def next_turn(self,player):
        if player == 'w':
            self.current_player = 'b'
        else:
            self.current_player = 'w'

    
    def neighbours(self, coord):
        return [self.board.goban[self.hand_to_coord(hand)[0]][self.hand_to_coord(hand)[1] - 1],
                self.board.goban[self.hand_to_coord(hand)[0] - 1][self.hand_to_coord(hand)[1]],
                self.board.goban[self.hand_to_coord(hand)[0]][self.hand_to_coord(hand)[1] + 1],
                self.board.goban[self.hand_to_coord(hand)[0] + 1][self.hand_to_coord(hand)[1]],]


    def capture (self, hand):
        if self.neighbours(hand) != ['0','0','0','0']:
            return True
