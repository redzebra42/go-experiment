from MCT import *
from rand_game_trees import *

if __name__ == "__main__":
    mct = MCT(RGTstate(), RGT())
    print(mct.tree_search(mct, 1, True))