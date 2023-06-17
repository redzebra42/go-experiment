import copy
import random
import numpy as np
import matplotlib.pyplot as plt
from MCT import *

def other_player(player):
    if player == "X":
        return "O"
    elif player == "O":
        return "X"
    else:
        return "error"

class TTT_state():

    def __init__(self, curr_player = "X", ttt_board =[["_","_","_"],
                                                      ["_","_","_"],
                                                      ["_","_","_"]]):
        self.ttt_board = copy.deepcopy(ttt_board)
        self.curr_player = curr_player

    def clone(self):
        new_child = TTT_state(self.curr_player, self.ttt_board)
        return new_child

    def next_turn(self):
        if self.curr_player == "X":
            self.curr_player = "O"
        else:
            self.curr_player = "X"

    def is_legal(self, coord):
        return self.ttt_board[coord[1]][coord[0]] == "_"

    def print(self):
        print("")
        for i in self.ttt_board:
            line = ""
            for j in i:
                line += j
            print(line)

class TTT():

    def other_player(self, player):
        if player == "X":
            return "O"
        elif player == "O":
            return "X"
        else:
            raise RuntimeError

    def play(self, state, move):
        if state.is_legal(move):
            state.ttt_board[move[1]][move[0]] = state.curr_player
            state.next_turn()
            # debug
            #state.print()
        else:
            raise RuntimeError

    def has_won(self, state):
        cp = self.other_player(state.curr_player)
        brd = state.ttt_board
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

    def is_over(self, state):
        return self.has_won(state)[0] or self.legal_moves(state) == []

    def winner(self, state):
        if self.is_over(state):
            return self.has_won(state)[1]

    def legal_moves(self, state):
        legal_moves = []
        l = len(state.ttt_board)
        for i in range(l):
            for j in range(l):
                move = (i, j)
                if state.is_legal(move):
                    legal_moves.append(move)
        return legal_moves

    def play_random(self, state):
        leg_moves = self.legal_moves(state)
        i = random.randint(0, len(leg_moves)-1)
        self.play(state, leg_moves[i])
    
    def rand_simulation(self, state):
        '''returns the new_state of the game after a randomly played game'''
        new_state = state.clone()
        while not self.is_over(new_state):
            self.play_random(new_state)
        return new_state


if __name__ == "__main__":
    ttt = TTT()
    ttt_state = TTT_state()
    mct = MCT(ttt, ttt_state)
    res_list = []
    x_coords = []
    for i in range(2):
        draws = 0
        for j in range(25):
            ttt_state = TTT_state()
            mct = MCT(ttt, ttt_state)
            while not ttt.is_over(ttt_state):
                #next_move = input("X to play ('xy' coords): ")
                #ttt.play(ttt_state, (int(next_move[0]), int(next_move[1])))
                #ttt_state.print()
                #mct.opponent_played(ttt_state)
                mct.new_move(4 + 8*i) # - mct.root.depth*(i//4)
                ttt_state = mct.root.state
                #ttt_state.print()
            if ttt.winner(ttt_state) == None:
                draws += 1
        print(i)
        res_list.append(draws)
        x_coords.append(5 + 4*i)
    print(res_list)
    print(x_coords)
    np_res_list = np.array(res_list)
    np_x_coords = np.array(x_coords)
    plt.plot(np_x_coords, np_res_list)
    plt.show()