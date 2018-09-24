"""Assignment 1 - Grocery Store Models

CSC148 Fall 2015, University of Toronto
Instructor: David Liu
Student: Graeme Stroud
Student number: 1002552944
---------------------------------------------

This file should contain all of the classes necessary to model the entities
in a grocery store.
"""
# This module is used to read in the data from a json configuration file.
import json


class GroceryStore:
    """A grocery store.

    Contains checkout lines with or without customers.
    """
    # === Private Attributes ===
    # @type _lines: list
    #     A list containing all the lines that a grocery store would have.
    # @type _line_capacity: int
    #    The maximum amount of people allowed in a line at once. Same capacity
    #    value for all lines in the store.

    def __init__(self, filename):
        """Initialize a GroceryStore from a configuration file <filename>.

        @type filename: str
            The name of the file containing the configuration for the
            grocery store.
        @rtype: None
        """

        self._lines = []

        with open(filename, 'r') as file:
            config = json.load(file)
        file.close()

        # <config> is now a dictionary with the keys 'cashier_count',
        # 'express_count', 'self_serve_count', and 'line_capacity'.

        self._line_capacity = config.pop("line_capacity")
        index = 0

        num_of_lines = config['cashier_count']
        for i in range(num_of_lines):
            self._lines.append(CashierLine())
            index += 1

        num_of_lines = config['express_count']
        for i in range(num_of_lines):
            self._lines.append(ExpressLine())
            index += 1

        num_of_lines = config['self_serve_count']
        for i in range(num_of_lines):
            self._lines.append(SelfServeLine())
            index += 1

    def add_customer(self, customer):
        """Adds a customer to one of the lines in the store. Returns the line
        they were added to.
        Precondition: the lines in the GroceryStore have one that has at least
        one free space
        @type self: GroceryStore
        @type customer: Customer
        @rtype: Line
        """

        shortest_line = None

        for line in self._lines:
            # Line is only eligible if it is not full.
            if len(line) < self._line_capacity:
                # Shortest line cannot be an ExpressLine when customer has more
                # than eight items.
                if (type(line) is not ExpressLine) or (customer.items < 8):
                    # Assumes first line that could take the customer is
                    # shortest.
                    if shortest_line is None:
                        shortest_line = line
                    # Finds another line later that could be shorter
                    elif len(line) < len(shortest_line):
                        shortest_line = line

        shortest_line.add_customer(customer)
        return shortest_line

    def checkout_complete(self, line):
        """Removes a customer from a line once they are at the front.

        @type line: Line
        @rtype: None
        """
        line.remove_first_customer()

    def first_customer_checkout_time(self, line):
        """Returns the amount of time needed to checkout for the first customer.
        in a line.
        @type self: GroceryStore
        @type line: Line
        @rtype: int
        """
        return line.checkout_time(line.get_first_customer().items)

    def close_line(self, index):
        """Closes line at <index> in the store. No new
        customers can join it (as new customers join the open lines only).

        Returns a list of the customers who have to move to a new line
        (the front of the list is the person who was at the back of the line).
        @type self: GroceryStore
        @type index: int
        @rtype: List[Customer]
        """

        moved_customers = []

        close_line = self._lines.pop(index)

        while len(close_line) > 1:
            moved_customers.append(close_line.pop_last_customer())

        return moved_customers


class Customer:
    """
    A class that represents a customer at a store

    === Attributes ===
    @type name: str
        The name or identity of the customer.
    @type items: int
        The number of items a Customer wants to checkout.
    @type entry_time: int
        The time when a Customer enters a line. It is always the time for
        the first line they enter.

    === Representation Invariants ===
    The number of items a customer has must be a natural number.
    """

    def __init__(self, name, items, timestamp):
        """A constructor for a Customer.
        @type self: Customer
        @type name: str
        @type items: int
        @type timestamp: int
        @rtype: None
        """
        self.name = name
        self.items = items
        self.entry_time = timestamp


class Line:
    """An abstract class not meant to be initialized in client code.
    Provides API for other lines of customers.
    """
    # === Private Attributes ===
    # @type: _customers: list
    #     A list of all the customers in the line.
    # === Representation Invariants ===
    # - The list should only contain type Customer

    def __init__(self):
        """Initializes a Line. Subclasses should be called instead of this.
        @type self: Line
        @rtype: None
        """
        self._customers = []

    def add_customer(self, customer):
        """Adds a customer to a line.
        @type self: Line
        @type customer: Customer
        @rtype:
        """
        self._customers.append(customer)

    def checkout(self, customer):
        """Takes customer out of line.
        @type self: Line
        @type customer: Customer
        @rtype: None
        """
        self._customers.remove(customer)

    def get_first_customer(self):
        """Returns the customer at the front of the line
        @type self: Line
        @rtype: Customer
        """
        return self._customers[0]

    def remove_first_customer(self):
        """Removes the first customer from the line
        @type self: Line
        @rtype: None
        """
        self._customers.pop(0)

    def pop_last_customer(self):
        """Removes and returns the last customer of the line.
        @type self: Line
        @rtype: Customer
        """
        return self._customers.pop()

    def checkout_time(self, items):
        """Returns the amount of time a customer will checkout in based on
        <items>.
         @type self: Line
         @type items: int
         @rtype: int
         """
        raise NotImplementedError

    def __len__(self):
        """Returns the number of customers in the line
        @type self: Line
        @rtype: int
        """
        return len(self._customers)

    def __str__(self):
        """Returns a string representation of this line

        @type self: Line
        @rtype: str
        """
        raise NotImplementedError


class CashierLine(Line):
    """A subclass of Line meant to represent a regular checkout line at a
    grocery store.

    Designed to take seven more seconds than the number of items a Customer has.

    """
    # === Private Attributes ===
    # @type: _customers: list
    #    A list of all the customers in the line.
    # === Representation Invariants ===
    # - The list should only contain type Customer

    def checkout_time(self, items):
        """Returns the amount of time a customer will checkout in based on
        <items>.
         @type self: CashierLine
         @rtype: int
         """
        return items + 7

    def __str__(self):
        """Returns a string representation of this line

        @type self: CashierLine
        @rtype: str
        """
        return "Cashier Line"


class ExpressLine(Line):
    """A subclass of Line for people with few items to checkout quicker.
    Designed to take 4 seconds longer than the number of items a Customer has.
    """
    # === Private Attributes ===
    # @type: customers: list
    #    A list of all the customers in the line.

    # === Representation Invariants ===
    # - The list should only contain type Customer
    # Each Customer in the line must have less than 8 items

    def add_customer(self, customer):
        """Adds a customer to a line.
        Can only do so if customer has less than 8 items.
        Otherwise, this method does nothing.

        @type customer: Customer
        @rtype: None
        """
        if customer.items < 8:
            self._customers.append(customer)

    def checkout_time(self, items):
            """Returns the amount of time a customer will checkout in based on
            <items>.
             @type self: ExpressLine
             @rtype: int
             """
            return items + 4

    def __str__(self):
        """Returns a string representation of this line

        @type self: ExpressLine
        @rtype: str
        """
        return "Express Line"


class SelfServeLine(Line):
    """A subclass of line meant to represent a self-checkout line at a Grocery
    store

    Designed to take a specific amount of time for a Customer to checkout:
    twice the amount of items they have plus one seconds.
    """
    # === Private Attributes ===
    # @type: _customers: list
    #    A list of all the customers in the line.
    # === Representation Invariants ===
    # - The list should only contain type Customer

    def checkout_time(self, items):
        """Returns the amount of time a customer will checkout in based on
        <items>.
         @type self: SelfServeLine
         @rtype: int
         """
        return 2*items + 1

    def __str__(self):
        """Returns a string representation of this line

        @type self: SelfServeLine
        @rtype: str
        """
        return "Self-Serve Line"

if __name__ == '__main__':
    store = GroceryStore('config.json')
    # Execute some methods here
    pass
