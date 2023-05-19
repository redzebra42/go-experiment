import copy
import random

class TTT():

    def __init__(self, ttt_board =[["_","_","_"],
                                   ["_","_","_"],
                                   ["_","_","_"]] ) -> None:
        self.ttt_board = copy.deepcopy(ttt_board)
        self.curr_player = "X"

    def print_ttt(self):
        print("")
        for i in self.ttt_board:
            line = ""
            for j in i:
                line += j
            print(line)
    
    def other_player(self, player):
        if player == "X":
            return "O"
        elif player == "O":
            return "X"
        else:
            return "error"

    def next_turn(self):
        if self.curr_player == "X":
            self.curr_player = "O"
        else:
            self.curr_player = "X"
    
    def is_legal(self,coord):
        return self.ttt_board[coord[1]][coord[0]] == "_"
    
    def move(self, coord):
        if self.is_legal(coord):
            self.ttt_board[coord[1]][coord[0]] = self.curr_player
            self.next_turn()
    
    def has_won(self):
        cp = self.other_player(self.curr_player)
        brd = self.ttt_board
        for i in range(len(brd)):
            if (brd[i][0], brd[i][1], brd[i][2]) == (cp, cp, cp):
                return (True, cp)
            elif (brd[0][i], brd[1][i], brd[2][i]) == (cp, cp, cp):
                return (True, cp)
        if (brd[0][0],brd[1][1],brd[2][2]) == (cp, cp, cp):
            return (True, cp)
        elif (brd[0][2],brd[1][1],brd[2][0]) == (cp, cp, cp):
            return (True, cp)
        return (False, None)
    
    def legal_moves(self):
        legal_moves = []
        l = len(self.ttt_board)
        for i in range(l):
            for j in range(l):
                coord = (i, j)
                if self.is_legal((i, j)):
                    legal_moves.append(coord)
        return legal_moves

    def play_random(self):
        leg_moves = self.legal_moves()
        i = random.randint(0, len(leg_moves))
        self.move(leg_moves[i-1])


if __name__ == "__main__":
    ttt = TTT()
    for i in range(9):
        ttt.play_random()
        ttt.print_ttt()
        print(ttt.has_won())
    