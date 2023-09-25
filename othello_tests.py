import unittest
from othello import *

o_game = Ogame()
board1 = Oboard()
b1 = [
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 3, 3, 2, 0, 0, 0],
    [0, 0, 3, 1, 2, 0, 0, 0],
    [0, 3, 1, 2, 2, 2, 0, 0],
    [0, 3, 0, 0, 1, 1, 0, 0],
    [0, 0, 0, 3, 3, 3, 3, 0],
    [0, 0, 0, 0, 0, 0, 0, 0]
      ]
b2 = [
    [0, 3, 3, 2, 1, 2, 3, 0],
    [0, 0, 2, 2, 2, 2, 3, 3],
    [0, 0, 1, 1, 1, 2, 2, 3],
    [3, 0, 1, 1, 1, 1, 0, 3],
    [3, 2, 1, 2, 1, 0, 0, 0],
    [3, 0, 1, 3, 2, 0, 0, 0],
    [0, 0, 1, 0, 3, 2, 0, 0],
    [0, 0, 0, 0, 0, 0, 3, 0]
      ]
board2 = Oboard(b1)
board3 = Oboard(b2, 1, 8, (2, 3))

class TestsOthello(unittest.TestCase):

    def test_is_legal(self):
        self.maxDiff = None
        legal_board = [[None for i in range(board1.size)] for j in range(board1.size)]
        for i in range(board1.size):
            for j in range(board1.size):
                legal_board[i][j] = board1.is_legal((i, j))
        expected_board = [
            [False, False, False, False, False, False, False, False],
            [False, False, False, False, False, False, False, False],
            [False, False, False, True, False, False, False, False],
            [False, False, True, False, False, False, False, False],
            [False, False, False, False, False, True, False, False],
            [False, False, False, False, True, False, False, False],
            [False, False, False, False, False, False, False, False],
            [False, False, False, False, False, False, False, False],
                          ]
        self.assertEqual(legal_board, expected_board)
    
    def test_is_legal_2(self):
        self.maxDiff = None
        legal_board = [[None for i in range(board2.size)] for j in range(board2.size)]
        for i in range(board2.size):
            for j in range(board2.size):
                legal_board[i][j] = board2.is_legal((i, j))
        expected_board = [
            [False, False, False, False, False, False, False, False],
            [False, False, False, False, False, False, False, False],
            [False, False, True, True, False, False, False, False],
            [False, False, True, False, False, False, False, False],
            [False, True, False, False, False, False, False, False],
            [False, True, False, False, False, False, False, False],
            [False, False, False, True, True, True, True, False],
            [False, False, False, False, False, False, False, False],
                          ]
        self.assertEqual(legal_board, expected_board)

    def test_legal_moves(self):
        board3.legal_moves()


if __name__ == "__main__":
    unittest.main()