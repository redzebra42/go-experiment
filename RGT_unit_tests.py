import unittest
from rand_game_trees import *
import math

test_tree_1 = RGT(RGTstate((0, 1), 5, 4))

class test_RGT(unittest.TestCase):

    def test_legal_moves(self):
        self.assertEqual(test_tree_1.state.enfants((0, 1)), [(1, 1), (1, 2), (1, 3), (1, 4)])
        self.assertEqual(test_tree_1.state.enfants((1, 1)), [(2, 1), (2, 2), (2, 3)])
        self.assertEqual(test_tree_1.state.enfants((1, 2)), [(2, 4), (2, 5), (2, 6)])
        self.assertEqual(test_tree_1.state.enfants((2, 5)), [(3, 9), (3, 10)])

    def test_parent(self):
        self.assertEqual(test_tree_1.state.parent((0, 1)), None)
        self.assertEqual(test_tree_1.state.parent((1, 1)), (0, 1))
        self.assertEqual(test_tree_1.state.parent((2, 2)), (1, 1))
        

    def test_path(self):
        path = test_tree_1.state.path
        for i in range(math.factorial(test_tree_1.state.board_size)):
            self.assertEqual(i, path(i)[test_tree_1.state.board_size - 2][1])
        for i in range(math.factorial(test_tree_1.state.board_size) - 1):
            for j in range(test_tree_1.state.board_size - 2):
                self.assertTrue(path(i)[j+1] in test_tree_1.state.enfants(path(i)[j]))


if __name__ == "__main__":
    unittest.main()