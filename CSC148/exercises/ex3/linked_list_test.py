# Exercise 3 - More Linked List Practice
#
# CSC148 Fall 2015, University of Toronto
# Instructor: David Liu
# ---------------------------------------------
"""Exercise 3, Task 1 TESTS.

Warning: This is an extremely incomplete set of tests!
Add your own to practice writing tests,
and to be confident your code is correct!
"""
import unittest
from linked_list_ex import LinkedList


class TestLinkedListEq(unittest.TestCase):

    def test_simple(self):
        list1 = LinkedList([1])
        list2 = LinkedList([1])

        # The following two tests do the same thing
        self.assertTrue(list1 == list2)
        self.assertTrue(list1.__eq__(list2))

    def test_same_length(self):
        list1 = LinkedList([2, 5, 10, -5, 4])
        list2 = LinkedList([2, 5, 10, -5, 10])

        self.assertFalse(list1 == list2)

    def test_one_empty(self):
        list1 = LinkedList([3])
        list2 = LinkedList([])
        self.assertFalse(list1 == list2)
        self.assertFalse(list2 == list1)

    def test_same(self):
        list1 = LinkedList([1,2,3,4,5])
        list2 = LinkedList([1,2,3,4,5])
        self.assertEqual(list1, list2)

    def test_diff(self):
        list1 = LinkedList([1,2,3,4,5])
        list2 = LinkedList([-1,2,3,4,5])
        self.assertNotEqual(list1, list2)



class TestLinkedListDeleteAll(unittest.TestCase):
    # NOTE: the tests will use the '__str__' method, so don't change the
    # implementation we've given you!

    def test_simple(self):
        lst = LinkedList([1, 2, 3])
        lst.delete_all(2)
        self.assertEqual(str(lst), '[1 -> 3]')

    def test_no_deletions(self):
        lst = LinkedList([1, 2, 3])
        lst.delete_all(4)
        self.assertEqual(str(lst), '[1 -> 2 -> 3]')

    def test_doctest(self):
        lst = LinkedList([1, 1, 2, 1, 3, 1, 1, 1])
        lst.delete_all(1)
        self.assertEqual(str(lst), '[2 -> 3]')


    def test_all_deleted(self):
        lst = LinkedList([1,1,1,1,1,1,1,1])
        lst.delete_all(1)
        self.assertEqual(str(lst), '[]')

    def test_complex(self):
        lst = LinkedList([1, 1, 2, 1, 1, 1, 1, 3, 1, 2, 4, 1, 3, 1, 2, 1, 1, 1])
        lst.delete_all(1)
        self.assertEqual(str(lst), '[2 -> 3 -> 2 -> 4 -> 3 -> 2]')



if __name__ == '__main__':
    unittest.main(exit=False)
