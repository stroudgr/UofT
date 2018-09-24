import unittest
from bst_ex import BinarySearchTree


class BSTItemsTest(unittest.TestCase):


    def test_one(self):
        bst = BinarySearchTree(1)
        self.assertEqual(bst.items_at_depth(1), [1])

    def test_empty(self):
        bst = BinarySearchTree(None)
        self.assertEqual(bst.items_at_depth(1), [])

    def test_big(self):
        bst = BinarySearchTree(10)
        bst.insert(5)
        bst.insert(1)
        bst.insert(7)
        bst.insert(20)
        bst.insert(30)
        bst.insert(25)
        bst.insert(45)
        self.assertEqual(bst.items_at_depth(3), [1, 7, 30])

    def test_empty_subtrees(self):
        bst = BinarySearchTree(1)
        self.assertEqual(bst.items_at_depth(1), [1])
        self.assertEqual(bst.items_at_depth(2), [])

    def test_incomplete_bst(self):
        bst = BinarySearchTree(10)
        bst.insert(1)
        bst.insert(0)
        bst.insert(15)
        bst.insert(20)
        bst.insert(17)
        bst.insert(9)
        #bst.print()
        self.assertEqual(bst.items_at_depth(1), [10])
        self.assertEqual(bst.items_at_depth(2), [1, 15])
        self.assertEqual(bst.items_at_depth(3), [0, 9, 20])
        self.assertEqual(bst.items_at_depth(4), [17])

    def test_final(self):
        bst = BinarySearchTree(15)
        bst.insert(10)
        bst.insert(8)
        bst.insert(9)
        bst.insert(11)
        bst.insert(21)
        bst.insert(22)
        bst.insert(23)
        bst.insert(24)
        bst.insert(25)
        bst.insert(17)
        bst.insert(18)
        self.assertEqual(bst.items_at_depth(1), [15])
        self.assertEqual(bst.items_at_depth(2), [10, 21])
        self.assertEqual(bst.items_at_depth(3), [8, 11, 17, 22])
        self.assertEqual(bst.items_at_depth(4), [9, 18, 23])
        self.assertEqual(bst.items_at_depth(5), [24])
        self.assertEqual(bst.items_at_depth(6), [25])


class BSTLevelsTest(unittest.TestCase):

    def test_one(self):
        bst = BinarySearchTree(1)
        self.assertEqual(bst.levels(), [(1, [1])])

    def test_empty(self):
        bst = BinarySearchTree(None)
        self.assertEqual(bst.levels(), [])

    def test_big(self):
        bst = BinarySearchTree(10)
        bst.insert(5)
        bst.insert(1)
        bst.insert(7)
        bst.insert(20)
        bst.insert(30)
        bst.insert(25)
        bst.insert(45)
        self.assertEqual(bst.levels(), [(1, [10]),
                                        (2, [5, 20]),
                                        (3, [1, 7, 30]),
                                        (4, [25, 45])])


    def test_incomplete_bst(self):
        bst = BinarySearchTree(10)
        bst.insert(1)
        bst.insert(0)
        bst.insert(15)
        bst.insert(20)
        bst.insert(17)
        bst.insert(9)
        bst.print()
        self.assertEqual(bst.levels(), [(1, [10]), (2, [1, 15]), (3, [0, 9, 20]), (4,[17])] )


    def test_final(self):
        bst = BinarySearchTree(15)
        bst.insert(10)
        bst.insert(8)
        bst.insert(9)
        bst.insert(11)
        bst.insert(21)
        bst.insert(22)
        bst.insert(23)
        bst.insert(24)
        bst.insert(25)
        bst.insert(17)
        bst.insert(18)
        self.assertEqual(bst.levels(), [(1, [15]), (2, [10, 21]), (3, [8, 11, 17, 22]), (4, [9, 18, 23]), (5, [24]), (6, [25])])

if __name__ == '__main__':
    unittest.main(exit=False)
