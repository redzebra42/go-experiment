from MCT import *
from rand_game_trees import *

if __name__ == "__main__":
    mct = MCT(RGT(), RGTstate())
    mct.new_move(1000)