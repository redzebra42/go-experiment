from go import *
import test_goban
import unittest
from MCT import *
from board import *

go = Go()
state = Board()
example_tree = MCT(go, state)
node_1 = Node(state)
example_tree.root.enfants = {(6, 6): Node(test_goban.Test_goban().state_1_1),
                             (2, 2): Node(test_goban.Test_goban().state_1_2)}
example_tree.root.enfants[(6, 6)].enfants = {(2, 2): Node(test_goban.Test_goban().state_2)}

class TestsGo(unittest.TestCase):
    '''
    def test_neighbour_0_0(self):
        self.go = Go()
        self.assertEqual(state.neighbours((0,0)), [(0,1), (1,0)])

    def test_neighbour_18_18(self):
        self.go = Go()
        self.assertEqual(state.neighbours((18,18)), [(18,17), (17,18)])

    def test_neighbour_0_4(self):
        self.go = Go()
        self.assertEqual(self.go.neighbours((0,4)), [(0,3), (0,5), (1,4)])

    def test_neighbour_10_12(self):
        self.go = Go()
        self.assertEqual(self.go.neighbours((10,12)), [(9,12), (11,12), (10,11), (10, 13)])

    def test_lib_1(self):
        self.go = Go()
        self.test_goban = test_goban.Test_goban()
        self.assertEqual(self.go.liberty(self.go.group((3, 3)))[0], 7)
        
    def test_lib_2(self):
        self.go = Go()
        self.test_goban = test_goban.Test_goban()
        self.assertEqual(self.go.liberty(self.go.group((3,17)))[0], 9)
    '''
    def test_group_1_1(self):
        tst_goban = test_goban.Test_goban().starting_board_3
        self.assertEqual(board.Board(tst_goban).group((1, 1)), [(1, 1), (2, 1), (1, 2), (0, 2), (0, 3)])

    def test_territory(self):
        state = board.Board(test_goban.Test_goban().starting_board_3)
        self.assertEqual(state.territory('b'), 19)
    
    def test_pretty_print(self):
        example_tree.pretty_print()

    def test_is_legal(self):
        state = board.Board(test_goban.Test_goban().starting_board_4)
        test_list = []
        test_list.append(go.is_legal(state, (0, 0)))
        test_list.append(go.is_legal(state, (8, 3)))
        test_list.append(go.is_legal(state, (5, 7)))
        test_list.append(go.is_legal(state, (8, 0)))
        test_list.append(go.is_legal(state, (1, 1)))
        test_list.append(go.is_legal(state, (2, 2)))
        test_list.append(go.is_legal(state, (8, 8)))
        self.assertEqual(test_list, [True, True, False, False, False, False, False])

    def test_is_suicide(self):
        self.maxDiff = None
        state = board.Board(test_goban.Test_goban().starting_board_4)
        test_list = [[] for k in range(state.size)]
        for i in range(state.size):
            for j in range(state.size):
                test_list[i].append((not state.is_suicide((j, i), 'w')) and state.is_legal((j, i), 'w'))
        res_list = [
            [True, True, True, True, True, True, True, True, True],
            [True, False, False, True, True, False, False, False, False],
            [False, False, False, False, False, False, False, False, False],
            [False, False, False, False, False, False, False, False, False],
            [False, True, True, False, False, False, False, False, False],
            [False, False, False, False, False, False, False, False, False],
            [False, False, False, False, False, False, False, False, False],
            [False, False, False, False, False, False, False, False, False],
            [False, False, False, True, False, False, False, False, False],
                    ]
        self.assertEqual(test_list, res_list)

if __name__ == "__main__":
    unittest.main()
