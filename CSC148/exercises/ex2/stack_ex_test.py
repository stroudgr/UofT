# Exercise 2 - More Stack Exercises
#
# CSC148 Fall 2015, University of Toronto
# Instructor: David Liu
# ---------------------------------------------
"""Exercise 2, Task 1 TESTS.

Warning: This is an extremely incomplete set of tests!
Add your own to practice writing tests,
and to be confident your code is correct!
"""
import unittest
from stack import Stack, EmptyStackError
from stack_ex import reverse_top_two, reverse, SmallStackError


class TestStack(unittest.TestCase):

    def test_simple_reverse_top_two(self):
        stack = Stack()
        stack.push(1)
        stack.push(2)
        reverse_top_two(stack)
        self.assertEqual(stack.pop(), 1)
        self.assertEqual(stack.pop(), 2)
        self.assertTrue(stack.is_empty())

    def test_reverse_two_empty(self):
        stack = Stack()
        # Note: this is a test which checks to see if an error is raised.
        with self.assertRaises(SmallStackError):
            # This code is run. A SmallStackError is expected to be raised here.
            reverse_top_two(stack)

    def test_simple_reverse(self):
        stack = Stack()
        stack.push(1)
        stack.push(2)
        reverse(stack)
        self.assertEqual(stack.pop(), 1)
        self.assertEqual(stack.pop(), 2)
        self.assertTrue(stack.is_empty())

    def test_reverse_empty(self):
        stack = Stack()
        reverse(stack)
        self.assertTrue(stack.is_empty())

    def test_reverse_one(self):
        stack = Stack()
        stack.push(1)
        reverse(stack)
        self.assertEqual(stack.pop(), 1)
        self.assertTrue(stack.is_empty())

    #TODO: Make more test cases

    def test_do_nothing(self):
        #check if stack is empty if nothing happens
        s = Stack()
        reverse(s)
        self.assertEqual(s._items, [])


    def test_list_is_reversed(self):
        s = Stack()
        for i in range(5):
            s.push(i+1)
        self.assertEqual(s._items, [1,2,3,4,5])

        reverse(s)
        self.assertEqual(s._items, [5,4,3,2,1])



    def test_only_top_two_reversed(self):
        s = Stack()
        for i in range(5):
            s.push(i+1)
        self.assertEqual(s._items, [1,2,3,4,5])

        expected_list = [1,2,3,5,4]

        reverse_top_two(s)

        self.assertEqual(s.pop(),expected_list.pop())
        self.assertEqual(s.pop(),expected_list.pop())
        self.assertEqual(s.pop(),expected_list.pop())
        self.assertEqual(s.pop(),expected_list.pop())
        self.assertEqual(s.pop(),expected_list.pop())


    def test_all_methods(self):
        #reverse all elements in stack
        #return nothing if stack is empty

        #flip top two elements in stack
        #raise error if less than two

        s = Stack()
        s.push(1)
        s.push(2)
        reverse_top_two(s)
        self.assertEqual(s._items, [2,1])
        s.pop()
        self.assertEqual(s._items, [2])

        with self.assertRaises(SmallStackError):
            reverse_top_two(s)
        s = Stack()
        s.push(2)
        s.pop()
        with self.assertRaises(SmallStackError):
            reverse_top_two(s)
        with self.assertRaises(EmptyStackError):
            s.pop()

        s.push(1)
        s.push(2)
        s.push(3)
        s.push(4)
        s.push(5)
        s.push(6)
        s.push(7)
        reverse_top_two(s)
        reverse(s)
        self.assertEqual(s._items, [6,7,5,4,3,2,1])

    def test_empty(self):
        s = Stack()
        with self.assertRaises(EmptyStackError):
            s.pop()
        s.push(1)
        self.assertEqual(1,s.pop())


if __name__ == '__main__':
    unittest.main(exit=False)
