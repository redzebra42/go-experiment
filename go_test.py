import go
import unittest

class TestGoMethods(unittest.TestCase):

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

if __name__ == "__main__":
    unittest.main()