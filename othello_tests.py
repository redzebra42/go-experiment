import unittest
from othello import *

o_game = Ogame()
board1 = Oboard()

class TestsOthello(unittest.TestCase):

    def is_legal_test(self):
        legal_board = [[None for i in range(board1.size)] for j in range(board1.size)]
        for i in range(board1.size):
            for j in range(board1.size):
                legal_board[i][j] = board1.is_legal((i, j))
        expected_board = [
            [False, False, False, False, False, False, False, False],
            [False, False, False, False, False, False, False, False],
            [False, False, False, False, True, False, False, False],
            [False, False, False, False, False, True, False, False],
            [False, False, True, False, False, False, False, False],
            [False, False, False, True, False, False, False, False],
            [False, False, False, False, False, False, False, False],
            [False, False, False, False, False, False, False, False],
                          ]
        self.assertEqual(legal_board, expected_board)

if __name__ == "__main__":
    unittest.main()