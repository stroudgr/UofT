# BinarySearchTree
#
# CSC148 Fall 2015, University of Toronto
# Instructor: David Liu
# ---------------------------------------------
"""Binary Search Tree from Week 8/9.

Note that this version of the class doesn't contain the lab exercises.
"""


class BinarySearchTree:
    """A Binary Search Tree."""
    # === Private Attributes ===
    # @type _root: object | None
    #     The root value stored in the BST, or None if the tree is empty.
    # @type _left: BinarySearchTree | None
    #     The left subtree, or None if the tree is empty.
    # @type _right: BinarySearchTree | None
    #     The right subtree, or None if the tree is empty.

    # === Representation Invariants ===
    # - If _root is None, then so are _left and _right.
    #   This represents an empty BST.
    # - If _root is not None, then _left and _right are BSTs, *not None*.
    # - Every item in _left is <= _root, and
    #   every item in _right is >= _root

    def __init__(self, root):
        """Initialize a new BST with a given root value.

        If <root> is None, the BST is empty.

        @type self: BinarySearchTree
        @type root: object | None
        @rtype: None
        """
        if root is None:
            self._root = None
            self._left = None
            self._right = None
        else:
            self._root = root
            self._left = BinarySearchTree(None)
            self._right = BinarySearchTree(None)

    def is_empty(self):
        """Return whether this tree is empty.

        @type self: BinarySearchTree
        @rtype: bool
        """
        return self._root is None

    def __contains__(self, item):
        """Return whether <item> is in this BST.

        @type self: BinarySearchTree
        @type item: object
        @rtype: bool
        """
        if self.is_empty():
            return False
        elif self._root == item:
            return True
        elif self._root > item:
            return self._left.__contains__(item)
        else:  # self._root < item
            return self._right.__contains__(item)

    def print(self, depth=0):
        """Print all of the items in this BST,
        where the root is printed before all of its subtrees,
        and every value is indented to show its depth.

        @type self: BinarySearchTree
        @rtype: None
        """
        if not self.is_empty():
            print(depth * '  ' + str(self._root))
            self._left.print(depth + 1)
            self._right.print(depth + 1)

    def insert(self, item):
        """Insert <item> into this tree in the correct location.

        Do not change positions of any other nodes.

        @type self: BinarySearchTree
        @type item: object
        @rtype: None
        """
        if self.is_empty():
            # Make new leaf.
            # Note that self._left and self._right cannot be None if the
            # tree is non-empty! (This is one of our invariants.)
            self._root = item
            self._left = BinarySearchTree(None)
            self._right = BinarySearchTree(None)
        elif item <= self._root:
            self._left.insert(item)
        else:
            self._right.insert(item)

    def delete_item(self, item):
        """Delete one occurrence of <item> from this BST.

        Do nothing if <item> is not in this BST.

        @type self: BinarySearchTree
        @type item: object
        @rtype: None
        """
        if self.is_empty():
            pass
        elif self._root == item:
            self.delete_root()
        elif self._root > item:
            self._left.delete_item(item)
        else:  # self._root < item
            self._right.delete_item(item)

    def delete_root(self):
        """Remove the root of this tree.

        Precondition: this tree is *non-empty*.

        @type self: BinarySearchTree
        @rtype: None
        """
        if self._left.is_empty() and self._right.is_empty():
            self._root = None
        elif self._left.is_empty():
            self._root = self._right.extract_min()
        else:
            self._root = self._left.extract_max()

    def extract_max(self):
        """Remove and return the maximum item stored in this tree.

        Precondition: this tree is *non-empty*.

        @type self: BinarySearchTree
        @rtype: object
        """
        if self._right.is_empty():
            temp = self._root
            # Copy left subtree to self, because root node is removed.
            # Note that self = self._left does NOT work!
            self._root = self._left._root
            self._right = self._left._right
            self._left = self._left._left
            return temp
        else:
            return self._right.extract_max()

    def extract_min(self):
        """Remove and return the minimum item stored in this tree.

        Precondition: this tree is *non-empty*.

        @type self: BinarySearchTree
        @rtype: object
        """
        if self._left.is_empty():
            temp = self._root
            self._root = self._right._root
            self._left = self._right._left
            self._right = self._right._right
            return temp
        else:
            return self._left.extract_min()

    # ---------------------------------------------------------------------
    # Exercise 5 questions
    # ---------------------------------------------------------------------
    def items_at_depth(self, d):
        """Return a sorted list of all items in this BST at depth <d>.

        Precondition: d >= 1.

        Reminder: you should not have to use the built-in 'sort' method
        or do any sorting yourself.

        @type self: BinarySearchTree
        @type d: int
        @rtype: list
        """
        if self.is_empty():
            return []
        elif d == 1:
            return [self._root]
        elif d < 1:
            raise ValueError
        else: # d > 1
            return self._left.items_at_depth(d-1) + self._right.items_at_depth(d-1)


        """
        if d == 1:
            if self.is_empty():
                return []
            else:
                return [self._root]
        elif not self.is_empty():
            result = []
            if not self._left.is_empty():
                result = result + self._left.items_at_depth(d-1)
            if not self._right.is_empty():
                result = result + self._right.items_at_depth(d-1)
            return result
        else:
            raise IndexError
        """

    def levels(self):
        """Return a list of items in the tree, separated by level.

        You may wish to use 'items_at_depth' as a helper method,
        but this also makes your code less efficient. Try doing
        this method twice, once with 'items_at_depth', and once
        without it!

        @type self: BinarySearchTree
        @rtype: list[(int, list)]
        """
        if self.is_empty():
            return []
        elif self._left.is_empty() and self._right.is_empty():
            return [(1, [self._root])]
        else:
            lst = [(1, [self._root])]
            left = self._left.levels() # a list
            right = self._right.levels()

            for i in range(max(len(left),len(right))):

                list_at_depth = []

                if i < len(left):
                    list_at_depth += left[i][1]

                if i < len(right):
                    list_at_depth += right[i][1]
                lst.append((i+2, list_at_depth))

            return lst
