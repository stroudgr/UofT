# Exercise 2 - More Stack Exercises
#
# CSC148 Fall 2015, University of Toronto
# Instructor: David Liu
# ---------------------------------------------
from stack import Stack, EmptyStackError
import copy


class SmallStackError(Exception):
    pass


def reverse_top_two(stack):
    """Reverse the top two elements on <stack>.

    Raise a SmallStackError if the stack has fewer than two items.

    @type stack: Stack
    @rtype: None

    >>> stack = Stack()
    >>> stack.push(1)
    >>> stack.push(2)
    >>> reverse_top_two(stack)
    >>> stack.pop()
    1
    >>> stack.pop()
    2
    """
    if stack.is_empty():
        raise SmallStackError
    old_top = stack.pop()
    if stack.is_empty():
        raise SmallStackError
    new_top = stack.pop()
    stack.push(old_top)
    stack.push(new_top)



def reverse(stack):
    """Reverse all the elements of <stack>.

    Do nothing if the stack is empty.

    @type stack: Stack
    @rtype: None

    >>> stack = Stack()
    >>> stack.push(1)
    >>> stack.push(2)
    >>> reverse(stack)
    >>> stack.pop()
    1
    >>> stack.pop()
    2
    """
    list = []
    while not stack.is_empty():
        list.append(stack.pop())
    while not len(list) == 0:
        stack.push(list.pop(0))

