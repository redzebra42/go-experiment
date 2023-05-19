import copy

class TTT():

    def __init__(self, ttt_board =[["X","X","X"],
                                   ["_","_","_"],
                                   ["X","_","_"]] ) -> None:
        self.ttt_board = copy.deepcopy(ttt_board)
        self.curr_player = "X"

    def print_ttt(self):
        for i in self.ttt_board:
            line = ""
            for j in i:
                line += j
            print(line)
        print("")
    
    def next_turn(self):
        if self.curr_player == "X":
            self.curr_player = "O"
        else:
            self.curr_player = "x"
    
    def is_legal(self,coord):
        return self.ttt_board[coord[1]][coord[0]] == "_"
    
    def move(self, coord):
        if self.is_legal(coord):
            self.ttt_board[coord[1]][coord[0]] = self.curr_player
            self.next_turn()
    
    def has_won(self):
        cp = self.curr_player
        brd = self.ttt_board
        for i in range(len(brd)):
            if (brd[i][0], brd[i][1], brd[i][2]) == (cp, cp, cp):
                return True
            elif (brd[0][i], brd[1][i], brd[2][i]) == (cp, cp, cp):
                return True
        if (brd[0][0],brd[1][1],brd[2][2]) == (cp, cp, cp):
            return True
        elif (brd[0][2],brd[1][1],brd[2][0]) == (cp, cp, cp):
            return True
        return False
            


if __name__ == "__main__":
    ttt = TTT()
    ttt.print_ttt()
    print(ttt.has_won())
    