import board

class Go():


    def __init__(self):
        self.board = board.Board()
        self.current_player = 'w'
        self.opp_player = 'b' if self.current_player == 'w' else 'w'
        

    def trans_hand(self,hand):
        self.list = ['a','b','c','d','e','f','g','h','j','k','l','m','n','o','p','q','r','s','t']
        for i in range(len(self.list)):
            if len(hand) == 2 and hand[0] == self.list[i]:
                return (i, int(hand[1])-1)
            elif len(hand) == 3 and hand[0] == self.list[i]:
                return (i, 10*int(hand[1]) + int(hand[2]) - 1)

    def move(self, hand):
        self.board.goban[self.trans_hand(hand)[1]][self.trans_hand(hand)[0]] = self.current_player

    def next_turn(self,player):
        if player == 'w':
            self.current_player = 'b'
        else:
            self.current_player = 'w'

    
    def neighbours(self,hand):
        return [self.board.goban[self.trans_hand(hand)[0]][self.trans_hand(hand)[1] - 1],
                self.board.goban[self.trans_hand(hand)[0] - 1][self.trans_hand(hand)[1]],
                self.board.goban[self.trans_hand(hand)[0]][self.trans_hand(hand)[1] + 1],
                self.board.goban[self.trans_hand(hand)[0] + 1][self.trans_hand(hand)[1]],]


    def capture (self, hand):
        if self.neighbours(hand) != ['0','0','0','0']:
            return True
