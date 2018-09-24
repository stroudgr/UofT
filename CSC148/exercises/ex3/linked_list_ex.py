# Exercise 3 - More Linked List Practice
#
# CSC148 Fall 2015, University of Toronto
# Instructor: David Liu
# ---------------------------------------------
"""Exercise 3, Task 1: More Linked List Practice.
"""


class _Node:
    """A node in a linked list.

    Note that this is considered a "private class", one
    which is only meant to be used in this module by the
    LinkedList class, but not by client code.

    === Attributes ===
    @type item: object
        The data stored in this node.
    @type next: _Node | None
        The next node in the list, or None if there are
        no more nodes in the list.
    """

    def __init__(self, item):
        """Initialize a new node storing <item>, with no next node.

        @type self: _Node
        @type item: object
        @rtype: None
        """
        self.item = item
        self.next = None  # Initially pointing to nothing


class LinkedList:
    """A linked list implementation of the List ADT.
    """
    # === Private Attributes ===
    # @type _first: _Node | None
    #     The first node in the list, or None if the list is empty.

    def __init__(self, items):
        """Initialize a new linked list containing the given items.

        The first node in the linked list contains the first item
        in <items>.

        @type self: LinkedList
        @type items: list
        @rtype: None
        """
        if len(items) == 0:  # No items, and an empty list!
            self._first = None
        else:
            self._first = _Node(items[0])
            current_node = self._first
            for item in items[1:]:
                current_node.next = _Node(item)
                current_node = current_node.next

    # ------------------------------------------------------------------------
    # Non-mutating methods: these methods do not change the list
    # ------------------------------------------------------------------------
    def is_empty(self):
        """Return whether this linked list is empty.

        @type self: LinkedList
        @rtype: bool
        """
        return self._first is None

    def __len__(self):
        """Return the number of elements in this list.

        @type self: LinkedList
        @rtype: int
        """
        curr = self._first
        size = 0
        while curr is not None:
            size += 1
            curr = curr.next
        return size

    def __getitem__(self, index):
        """Return the item at position index in this list.

        Raise IndexError if <index> is >= the length of this list.

        @type self: LinkedList
        @type index: int
        @rtype: object
        """
        curr = self._first
        curr_index = 0

        # Iterate to (index)-th node
        while curr is not None and curr_index < index:
            curr = curr.next
            curr_index += 1

        if curr is None:
            raise IndexError
        else:
            return curr.item

    def __str__(self):
        """Return a string representation of this list.

        The string is in the form '[item1 -> item2 -> ... -> item-n]'.

        @type self: LinkedList
        @rtype: str

        >>> lst = LinkedList([1, 2, 3])
        >>> str(lst)
        '[1 -> 2 -> 3]'
        """
        items = []
        curr = self._first
        while curr is not None:
            items.append(str(curr.item))
            curr = curr.next
        return '[' + ' -> '.join(items) + ']'

    # ------------------------------------------------------------------------
    # Mutating methods: these methods modify the list
    # ------------------------------------------------------------------------

    def pop(self, index):
        """Remove node at position <index> and return its item.

        Raise IndexError if <index> is >= the length of <self>.
        Precondition: <index> >= 0.

        @type self: LinkedList
        @type index: int
        @rtype: object
        """
        if len(self) <= index:
            raise IndexError

        if index == 0:
            # TODO: Complete this part of the code!
            pass
        else:
            # Get the node at position (index - 1)
            curr_index = 0
            curr = self._first
            while curr is not None and curr_index < index - 1:
                curr = curr.next
                curr_index = curr_index + 1

            if curr is None:
                raise IndexError
            else:
                if curr.next is None:
                    raise IndexError
                else:
                    # curr is the node at index - 1
                    popped_item = curr.next.item
                    curr.next = curr.next.next
                    return popped_item

    def insert(self, index, item):
        """Insert a new node containing item at position <index>.

        Raise IndexError if <index> is > the length of this list.
        Note that adding to the end of a linked list is okay.
        Precondition: <index> >= 0.

        @type self: LinkedList
        @type index: int
        @type item: object
        @rtype: None
        """
        if index > len(self):
            raise IndexError

        # Create new node containing the item
        new_node = _Node(item)

        if index == 0:
            new_node.next = self._first
            self._first = new_node
        else:
            # Get the node at position (index - 1)
            curr_index = 0
            curr = self._first
            while curr is not None and curr_index < index - 1:
                curr = curr.next
                curr_index = curr_index + 1

            if curr is None:
                raise IndexError
            else:
                new_node.next = curr.next
                curr.next = new_node

    # ------------------------------------------------------------------------
    # Exercise 3: Implement the following two methods.
    # ------------------------------------------------------------------------
    def __eq__(self, other):
        """Return whether <self> and <other> contain the same elements.

        You may compare the items of the lists using ==.

        This is a special method: overriding this method allows you to
        compare linked lists using ==.

        WARNING: don't assume the two lists have the same length!

        @type self: LinkedList
        @type other: LinkedList
        @rtype: bool

        >>> linked1 = LinkedList([1, 2, 3])
        >>> linked2 = LinkedList([1, 2, 3])
        >>> linked1 == linked2 # Same as linked1.__eq__(linked2)
        True
        """
        curr1 = self._first
        curr2 = other._first

        while curr1 is not None and curr2 is not None:
            if curr1.item != curr2.item:
                return False
            curr1 = curr1.next
            curr2 = curr2.next

        if curr1 != curr2:
            return False
        else:
            return True


    def delete_all(self, item):
        """Delete *all* occurrences of <item> in <self>.

        Do nothing if <item> doesn't appear in <self>.
        Use == to compare <item> with the items in <self>.

        NOTE: Be careful when there are consecutive nodes which
        all contain <item>! Don't miss any!

        Hint: also, you might end up deleting the first node.
        Pay attention to this corner case, and make sure you're updating
        self._first appropriately.

        @type self: LinkedList
        @type item: object
        @rtype: None

        >>> linky = LinkedList([2, 1, 1, 2, 1, 3, 1, 1, 1])
        >>> linky.delete_all(1)
        >>> str(linky)
        '[2 -> 2 -> 3]'
        """

        curr = self._first
        previous = None
        while curr is not None:

            if curr.item == item:
                # Removes first item in list
                if previous is None:
                    self._first = curr.next
                    curr = self._first

                else:
                    previous.next = curr.next
                    curr = curr.next
            else:
                previous = curr
                curr = curr.next

