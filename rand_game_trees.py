import random
import math

global_size = 7

'''
game class that has the following functions:
legal_moves(state)
play_at(state, move)
is_over(state)
winner(state)
rand_simulation(state)
play_mct()

state class with the following functions:
curr_player()
clone()
'''

class RGTstate():

    def __init__(self, position=(0, 1), best_move=random.randint(1, math.factorial(global_size)), board_size=global_size) -> None:
        self.board_size = board_size
        self.best_move = best_move
        self.position = position
    
    def best_path(self):
        nb_tot_moves = (math.factorial(self.board_size))
        frac = self.best_move/nb_tot_moves
        path = []
        for i in range(self.board_size - 1):
            largeur = nb_tot_moves/math.factorial(self.board_size - i - 1)
            j = 0
            while j/largeur < frac:
                j += 1
            path.append((i + 1, j))
        return path



    def curr_player(self):
        return self.position[0] % 2

    def clone(self):
        return RGTstate(self.position, self.best_move, self.board_size)

class RGT():
    """
    game tree represented by nodes with coordinates (depth, index) with depth of root = 0 and indexes 
    starting at 1 from left up to board_size!/(totaldepth-depth)! 
    """
    def __init__(self, state=RGTstate()) -> None:
        self.state = state

    def legal_moves(self, state):
        leg_pos = []
        for i in range(self.state.board_size - state.position[0]):
            leg_pos.append((state.position[0] + 1, (state.position[1] - 1) * (state.position[0] + 1) + i + 1))
        return leg_pos

    def play_at(self, state, move):
        state.position = move

    def is_over(self, state):
        return state.position[0] == state.board_size - 1

    def winner(self, state):
        pass

    def rand_simulation(self, state):
        pass

    def play_mct(self):
        pass
        
if __name__ == "__main__":
    pos = (3, 5)
    state = RGTstate(pos)
    rgt = RGT(state)

    print(rgt.legal_moves(state))
    rgt.play_at(state, (4,18))
    print(rgt.legal_moves(state))
    print(rgt.is_over(state))
    rgt.play_at(state, (7,34))
    print(rgt.legal_moves(state))
    print(rgt.is_over(state))
    print(state.best_move)
    print(state.best_path())
