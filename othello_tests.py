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
board2 = Oboard(b1)

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
        board1.print_board()
        for line in legal_board:
            print(line)
        print("")
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
        board2.print_board()
        for line in legal_board:
            print(line)
        self.assertEqual(legal_board, expected_board)


if __name__ == "__main__":
    unittest.main()