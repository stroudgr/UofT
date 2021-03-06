# Exercise 4 - More Tree Practice
#
# CSC148 Fall 2015, University of Toronto
# Instructor: David Liu
# ---------------------------------------------
"""Exercise 4: More Tree Practice.
"""


class Tree:
    """A recursive tree data structure.

    Note the relationship between this class and LinkedListRec
    from Lab 5; the only major difference is that self._rest
    has been replaced by self._subtrees to handle multiple
    recursive sub-parts.
    """
    # === Private Attributes ===
    # @type _root: object | None
    #     The item stored at the tree's root, or None if the tree is empty.
    # @type _subtrees: list[Tree]
    #     A list of all subtrees of the tree

    # === Representation Invariants ===
    # - If self._root is None then self._subtrees is empty.
    #   This setting of attributes represents an empty Tree.
    # - self._subtrees does not contain any empty Trees.

    def __init__(self, root):
        """Initialize a new Tree with the given root value.

        If <root> is None, the tree is empty.
        A new tree always has no subtrees.

        @type self: Tree
        @type root: object
        @rtype: None
        """
        self._root = root
        self._subtrees = []

    # ------------------------------------------------------------------------
    # Non-mutating methods
    # ------------------------------------------------------------------------

    def is_empty(self):
        """Return True if this tree is empty.

        @type self: Tree
        @rtype: bool
        """
        return self._root is None

    def add_subtrees(self, new_trees):
        """Add the trees in <new_trees> as subtrees of this tree.

        Raise ValueError if this tree is empty.

        @type self: Tree
        @type new_trees: list[Tree]
        @rtype: None
        """
        if self.is_empty():
            raise ValueError()
        else:
            self._subtrees.extend(new_trees)

    def __len__(self):
        """Return the number of nodes contained in this tree.

        @type self: Tree
        @rtype: int
        """
        if self.is_empty():
            return 0
        else:
            size = 1
            for subtree in self._subtrees:
                size += subtree.__len__()
            return size

    # You may find this method helpful for debugging.
    def print_tree(self):
        """Print all of the items in this tree.

        For each node, its item is printed before any of its
        descendants' items. The output is nicely indented.

        @type self: Tree
        @rtype: None
        """
        if not self.is_empty():
            # This prints the root item before all of the subtrees.
            print(self._root)
            for subtree in self._subtrees:
                subtree.print_tree()

                # Or alternately, simply call
                # self.print_tree_indent()

    def print_tree_indent(self, depth=0):
        """Print all of the items in this tree at a set indentation level.

        @type self: Tree
        @rtype: None
        """
        if not self.is_empty():
            print(depth * '  ' + str(self._root))
            for subtree in self._subtrees:
                subtree.print_tree_indent(depth + 1)

    # ------------------------------------------------------------------------
    # Mutating methods
    # ------------------------------------------------------------------------

    def delete_root(self):
        """Remove the root item of this tree.

        @type self: Tree
        @rtype: None
        """
        if len(self._subtrees) == 0:
            # Base case when empty or just one node
            self._root = None
        else:
            chosen_subtree = self._subtrees[0]
            self._root = chosen_subtree._root
            self._subtrees = (chosen_subtree._subtrees +
                              self._subtrees[1:])

    # We will cover this method on Friday.
    def delete_item(self, item):
        """Delete *one* occurrence of item from this tree.
        Return True if item was deleted, and False otherwise.

        @type self: Tree
        @type item: object
        @rtype: bool
        """
        if self.is_empty():
            return False
        else:
            if self._root == item:
                self.delete_root()
                return True
            else:
                for subtree in self._subtrees:
                    # Try to delete item from current subtree
                    # If it works, return!
                    if subtree.delete_item(item):
                        # If the subtree is now empty, remove it!
                        if subtree.is_empty():
                            self._subtrees.remove(subtree)
                        return True
                return False

    # ------------------------------------------------------------------------
    # Exercise 4, Task 1
    # ------------------------------------------------------------------------
    def __eq__(self, other):
        """Return whether <self> and <other> are equal.

        @type self: Tree
        @type other: Tree
        @rtype: bool
        >>> s = Tree(1)
        >>> t = Tree(1)
        >>> s == t
        True
        >>> subtrees = [Tree(4), Tree(5)]
        >>> s.add_subtrees(subtrees)
        >>> s==t
        False
        >>> t.add_subtrees(subtrees)
        >>> s==t
        True
        >>> t = Tree(None)
        >>> s==t
        False
        >>> s = Tree(None)
        >>> s==t
        True
        """

        # Won't be true if trees aren't the same length!
        if len(self) != len(other):
            return False

        else:
            # Different roots means the trees are different
            if self._root != other._root:
                return False
            # Returns whether the subtrees are the same
            # This can make a recursive call, based on the implementation
            # of list comparisons in Python.
            else:
                return self._subtrees == other._subtrees
            """
            # Same function as above return statement.
            elif len(self._subtrees) != len(other._subtrees):
                return False
            else:
                for i in range(len(self._subtrees)):
                    if not (self._subtrees[i] == other._subtrees[i]):
                        return False
                return True"""

    # ------------------------------------------------------------------------
    # Exercise 4, Task 2
    # ------------------------------------------------------------------------
    def to_nested_list(self):
        """Return the nested list representation of this tree.

        @type self: Tree
        @rtype: list
        >>> t = Tree(1)
        >>> t.to_nested_list()
        [1]
        >>> t.add_subtrees([Tree(2),Tree(3)])
        >>> t.to_nested_list()
        [1, [2], [3]]
        >>> st = Tree(4)
        >>> st.add_subtrees([Tree(5), Tree(6)])
        >>> t.add_subtrees([st])
        >>> t.to_nested_list()
        [1, [2], [3], [4, [5], [6]]]
        """

        nested_list = []

        if self.is_empty():
            return nested_list

        else:
            nested_list.append(self._root)
            for subtree in self._subtrees:
                nested_list.append(subtree.to_nested_list())
            return nested_list




def to_tree(obj):
    """Return the Tree which <obj> represents.

    Precondition: <obj> is a valid nested list representation of a tree.

    You may not access Tree attributes directly. This function can be
    implemented only using the Tree constructor and add_subtrees methods.

    @type obj: list
    @rtype: Tree
    >>> l = []
    >>> t = to_tree(l)
    >>> t.print_tree()
    >>> l = [1]
    >>> t = to_tree(l)
    >>> isinstance(t, Tree)
    True
    >>> t.print_tree()
    1

    >>> t = to_tree([1, [2], [3], [4, [5], [6]]])
    >>> t.print_tree()
    1
    2
    3
    4
    5
    6
    """
    if len(obj) == 0:
        return Tree(None)
    if len(obj) == 1:
        return Tree(obj[0])
    else:
        t = Tree(obj[0])
        subtrees = []
        for nested_list in obj:
            if not isinstance(nested_list, int):
                subtrees.append(to_tree(nested_list))
        t.add_subtrees(subtrees)
        return t

