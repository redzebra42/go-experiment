import unittest
from rand_game_trees import *
import math

test_tree_1 = RGT(RGTstate((0, 1), 5, 4))

class test_RGT(unittest.TestCase):

    def test_legal_moves(self):
        self.assertEqual(test_tree_1.state.enfants((0, 0)), [(1, 0), (1, 1), (1, 2), (1, 3)])
        self.assertEqual(test_tree_1.state.enfants((1, 0)), [(2, 0), (2, 1), (2, 2)])
        self.assertEqual(test_tree_1.state.enfants((1, 1)), [(2, 3), (2, 4), (2, 5)])
        self.assertEqual(test_tree_1.state.enfants((2, 4)), [(3, 8), (3, 9)])

    def test_best_path(self):
        best_path = test_tree_1.state.path
        for i in range(math.factorial(test_tree_1.state.board_size)):
            self.assertEqual(i, best_path(i)[test_tree_1.state.board_size - 2][1])
        for i in range(math.factorial(test_tree_1.state.board_size) - 1):
            for j in range(test_tree_1.state.board_size):
                self.assertTrue(best_path(i)[j+1] in test_tree_1.state.enfants(best_path(i)[j]))


if __name__ == "__main__":
    unittest.main()