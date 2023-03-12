import go
import test_goban
import unittest

class TestGoNeighbours(unittest.TestCase):

    def test_neighbour_0_0(self):
        self.go = go.Go()
        self.assertEqual(self.go.neighbours((0,0)), [(0,1), (1,0)])

    def test_neighbour_18_18(self):
        self.go = go.Go()
        self.assertEqual(self.go.neighbours((18,18)), [(18,17), (17,18)])

    def test_neighbour_0_4(self):
        self.go = go.Go()
        self.assertEqual(self.go.neighbours((0,4)), [(0,3), (0,5), (1,4)])

    def test_neighbour_10_12(self):
        self.go = go.Go()
        self.assertEqual(self.go.neighbours((10,12)), [(9,12), (11,12), (10,11), (10, 13)])


class TestGoGroups(unittest.TestCase):

    def test_group_1(self):
        self.go = go.Go()
        self.test_goban = test_goban.Test_goban()
        self.assertEqual(self.go.group((3, 3), self.test_goban.goban_1), [(3, 3), (4, 3), (3, 4), (3, 5)])

    def test_group_2(self):
        self.go = go.Go()
        self.test_goban = test_goban.Test_goban()
        self.assertEqual(self.go.group((3, 17), self.test_goban.goban_2), [(3, 3), (4, 3), (3, 4), (3, 5)])


if __name__ == "__main__":
    unittest.main()
