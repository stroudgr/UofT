import unittest
#from tree_ex import Tree, to_tree
from submission import Tree, to_tree

class TreeEqTest(unittest.TestCase):

    def test_ones(self):
        tree1 = Tree(1)
        tree2 = Tree(1)
        self.assertTrue(tree1 == tree2)

    def test_empty(self):
        tree1 = Tree(1)
        treeEmp = Tree(None)
        self.assertFalse(treeEmp, tree1)

    def test_empty_two(self):
        tree1 = Tree(None)
        tree2 = Tree(None)
        self.assertTrue(tree1 == tree2)

    def test_big(self):
        t1 = Tree(1)
        t2 = Tree(2)
        t3 = Tree(3)
        t4 = Tree(4)
        t5 = Tree(5)
        t1.add_subtrees([t2, t4])
        t2.add_subtrees([t3, t5])

        o1 = Tree(1)
        o2 = Tree(2)
        o3 = Tree(3)
        o4 = Tree(4)
        o5 = Tree(5)
        o1.add_subtrees([o2, o4])
        o2.add_subtrees([o3, o5])
        self.assertTrue(t1 == o1)


    def test_big_false(self):
        t1 = Tree(1)
        t2 = Tree(2)
        t3 = Tree(3)
        t4 = Tree(2)
        t5 = Tree(5)
        t1.add_subtrees([t2, t4])
        t2.add_subtrees([t3, t5])

        o1 = Tree(1)
        o2 = Tree(2)
        o3 = Tree(3)
        o4 = Tree(4)
        o5 = Tree(5)
        o1.add_subtrees([o2, o4])
        o2.add_subtrees([o3, o5])
        self.assertTrue(t1 != o1)


    def test_big_backwards(self):
        t1 = Tree(1)
        t2 = Tree(2)
        t3 = Tree(3)
        t4 = Tree(4)
        t5 = Tree(5)
        t1.add_subtrees([t2, t4])
        t2.add_subtrees([t3, t5])

        o1 = Tree(1)
        o2 = Tree(2)
        o3 = Tree(3)
        o4 = Tree(4)
        o5 = Tree(5)
        o1.add_subtrees([o4, o2])
        o2.add_subtrees([o3, o5])
        self.assertTrue(t1 != o1)

class ToNestedListTest(unittest.TestCase):

    def test_one(self):
        t = Tree(1)
        self.assertEqual(t.to_nested_list(), [1])

    def test_empty(self):
        t = Tree(None)
        self.assertEqual(t.to_nested_list(), [])

    def test_big(self):
        t1 = Tree(1)
        t2 = Tree(2)
        t3 = Tree(3)
        t4 = Tree(4)
        t5 = Tree(5)
        t1.add_subtrees([t2, t4])
        t2.add_subtrees([t3, t5])

        self.assertEqual(t1.to_nested_list(), [1, [2, [3], [5]], [4]])

    def test_big_two(self):
        t1 = Tree(1)
        t2 = Tree(2)
        t3 = Tree(3)
        t4 = Tree(4)
        t5 = Tree(5)
        t1.add_subtrees([t2, t4, t3])
        t2.add_subtrees([t5])
        t3.add_subtrees([t5])
        t4.add_subtrees([t5])

        self.assertEqual(t1.to_nested_list(), [1, [2, [5]], [4, [5]], [3, [5]]])


class ToTreeTest(unittest.TestCase):

    def test_one(self):
        t = to_tree([1])
        self.assertEqual(t._root, 1)
        self.assertEqual(t._subtrees, [])

    def test_empty(self):
        t = to_tree([])
        self.assertTrue(t.is_empty())

    def test_big(self):
        t = to_tree([1, [2, [3], [5]], [4]])
        self.assertEqual(t._root, 1)
        self.assertEqual(t._subtrees[0]._root, 2)
        self.assertEqual(t._subtrees[1]._root, 4)
        self.assertEqual(t._subtrees[0]._subtrees[0]._root, 3)
        self.assertEqual(t._subtrees[0]._subtrees[1]._root, 5)

        # Note: we will use the __len__ method to test, so don't change it!
        self.assertEqual(len(t), 5)

    def test_big_two(self):
        t = to_tree([1, [2, [5]], [4, [5]], [3, [5]]])
        self.assertEqual(t._root, 1)
        self.assertEqual(t._subtrees[0]._root, 2)
        self.assertEqual(t._subtrees[1]._root, 4)
        self.assertEqual(t._subtrees[2]._root, 3)
        self.assertEqual(t._subtrees[0]._subtrees[0]._root, 5)
        self.assertEqual(t._subtrees[1]._subtrees[0]._root, 5)
        self.assertEqual(t._subtrees[2]._subtrees[0]._root, 5)


        # Note: we will use the __len__ method to test, so don't change it!
        self.assertEqual(len(t), 7)

if __name__ == '__main__':
    unittest.main(exit=False)
