# Assignment 2 - Puzzle Game
#
# CSC148 Fall 2015, University of Toronto
# Instructor: David Liu
# ---------------------------------------------
"""Sudoku puzzle module.

Here are the rules of Sudoku:

- The puzzle consists of an n-by-n grid, where n = 4, 9, 16, or 25.
  Each square contains a uppercase letter between A and the n-th letter
  of the alphabet, or is empty.
  For example, on a 4-by-4 Sudoku board, the available letters are
  A, B, C, or D. On a 25-by-25 board, every letter A-Y is available.
- The goal is to fill in all empty squares with available letters so that
  the board has the following property:
    - no two squares in the same row have the same letter
    - no two squares in the same column have the same letter
    - no two squares in the same *subsquare* has the same letter
  A *subsquare* is found by dividing the board evenly into sqrt(n)-by-sqrt(n)
  pieces. For example, a 4-by-4 board would have 4 subsquares: top left,
  top right, bottom left, bottom right.

"""
from puzzle import Puzzle
from math import sqrt

CHARS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'


class SudokuPuzzle(Puzzle):
    """Implementation of a Sudoku puzzle."""
    # === Private Attributes ===
    # @type _n: int
    #     The size of the board. Must be 4, 9, 16, or 25.
    # @type _grid: list[list[str]]
    #     A representation of the Sudoku grid. Consists of a list of lists,
    #     where each inner list represents a row of the grid.
    #
    #     Each item of the inner list is either an uppercase letter,
    #     or is the empty string '', representing an empty square.
    #     Each letter must be between 'A' and the n-th letter of the alphabet.
    def __init__(self, grid):
        """Create a new Sudoku puzzle with an initial grid 'grid'.

        Precondition: <grid> is a valid Sudoku grid.

        @type self: SudokuPuzzle
        @type grid: list[list[str]]
        @rtype: None
        """
        self._n = len(grid)
        self._grid = grid

    def __str__(self):
        """Return a human-readable string representation of <self>.

        Note that the numbers at the top and left cycle 0-9,
        to help the user when they want to enter a move.

        @type self: SudokuPuzzle
        @rtype: str

        >>> s = SudokuPuzzle([['A', 'B', 'C', 'D'], \
                              ['D', 'C', 'B', 'A'], \
                              ['', 'D', '', ''],\
                              ['', '', '', '']])
        >>> print(s)
          01|23
         ------
        0|AB|CD
        1|DC|BA
         ------
        2| D|
        3|  |
        <BLANKLINE>
        """
        m = int(sqrt(self._n))
        s = ''
        # Column label
        s += '  '
        for col in range(self._n):
            s += str(col % 10)
            # Vertical divider
            if (col + 1) % m == 0 and col + 1 != self._n:
                s += '|'
        # Horizontal divider
        s += '\n ' + ('-' * (self._n + m)) + '\n'
        for i in range(self._n):
            # Row label
            s += str(i % 10) + '|'
            for j in range(self._n):
                cell = self._grid[i][j]
                if cell == '':
                    s += ' '
                else:
                    s += str(cell)
                # Vertical divider
                if (j + 1) % m == 0 and j + 1 != self._n:
                    s += '|'
            s = s.rstrip()
            s += '\n'

            # Horizontal divider
            if (i + 1) % m == 0 and i + 1 != self._n:
                s += ' ' + ('-' * (self._n + m)) + '\n'

        return s

    def is_solved(self):
        """Return whether <self> is solved.

        A Sudoku puzzle is solved if its state matches the criteria
        listed at the end of the puzzle description.

        @type self: SudokuPuzzle
        @rtype: bool

        >>> s = SudokuPuzzle([['A', 'B', 'C', 'D'], \
                              ['C', 'D', 'A', 'B'], \
                              ['B', 'A', 'D', 'C'], \
                              ['D', 'C', 'B', 'A']])
        >>> s.is_solved()
        True
        >>> s = SudokuPuzzle([['A', 'B', 'C', 'D'], \
                              ['C', 'D', 'A', 'B'], \
                              ['B', 'D', 'A', 'C'], \
                              ['D', 'C', 'B', 'A']])
        >>> s.is_solved()
        False
        """
        # Check for empty cells
        for row in self._grid:
            if '' in row:
                return False

        # Check rows
        for row in self._grid:
            if sorted(row) != list(CHARS[:self._n]):
                return False

        # Check cols
        for i in range(self._n):
            # Note the use of a list comprehension here.
            if sorted([row[i] for row in self._grid]) != list(CHARS[:self._n]):
                return False

        # Check all subsquares
        m = int(sqrt(self._n))
        for x in range(0, self._n, m):
            for y in range(0, self._n, m):
                items = [self._grid[x + i][y + j]
                         for i in range(m)
                         for j in range(m)]

                if sorted(items) != list(CHARS[:self._n]):
                    return False

        # All checks passed
        return True

    def extensions(self):
        """Return list of extensions of <self>.

        This method picks the first empty cell (looking top-down,
        left-to-right) and returns a list of the new puzzle states
        obtained by filling in the empty cell with one of the
        available letters that does not violate any of the constraints
        listed in the problem description. (E.g., if there is
        already an 'A' in the row with the empty cell, this method should
        not try to fill in the cell with an 'A'.)

        If there are no empty cells, returns an empty list.

        @type self: SudokuPuzzle
        @rtype: list[SudokuPuzzle]

        >>> s = SudokuPuzzle([['A', 'B', 'C', 'D'], \
                              ['C', 'D', 'A', 'B'], \
                              ['B', 'A', '', ''], \
                              ['D', 'C', '', '']])
        >>> lst = list(s.extensions())
        >>> len(lst) # Can only put D into (2, 2)
        1
        >>> print(lst[0])
          01|23
         ------
        0|AB|CD
        1|CD|AB
         ------
        2|BA|D
        3|DC|
        <BLANKLINE>
        """
        # Search for the first empty cell
        row_index, col_index = None, None
        for i in range(self._n):
            row = self._grid[i]
            if '' in row:
                row_index, col_index = i, row.index('')
                break

        if row_index is None:
            return []
        else:
            # Calculate possible letter to fill the empty cell
            letters = self._possible_letters(row_index, col_index)
            return [self._extend(letter, row_index, col_index)
                    for letter in letters]

    # ------------------------------------------------------------------------
    # Helpers for method 'extensions'
    # ------------------------------------------------------------------------
    def _possible_letters(self, row_index, col_index):
        """Return a list of the possible letters for a cell.

        The returned letters must be a subset of the available letters.
        The returned list should be sorted in alphabetical order.

        @type self: SudokuPuzzle
        @type row_index: int
        @type col_index: int
        @rtype: list[str]

        >>> s = SudokuPuzzle([['D', 'A', '', ''],\
                              ['', '', '', ''],\
                              ['C', 'D', 'A', 'B'],\
                              ['A', 'B', 'C', 'D']])
        >>> s._possible_letters(0, 2)
        ['B']
        >>> s._possible_letters(0, 3)
        ['C']
        """
        letters = []

        # Only checks as many letters as possible in the grid.
        for letter in list(CHARS[:self._n]):

            possible = True

            for i in range(self._n):

                # Letter is not in the same column <col_index> for any row.
                # Letter is not in the same row <row_index> for any column.
                if self._grid[i][col_index] == letter or \
                                self._grid[row_index][i] == letter:
                    possible = False
                    break

            if possible:
                # Compares with every element in the same sub-square.

                n = int(sqrt(self._n))

                # Goes from the lowest row to the highest in the square
                for x in range(n*(row_index//n), n*(row_index//n) + n):

                    # Goes from the lowest column to the highest
                    for y in range(n*(col_index//n), n*(col_index//n) + n):

                        if self._grid[x][y] == letter:
                            possible = False
                            break
                    if not possible:
                        break

            if possible and self._grid[row_index][col_index] == '':
                letters.append(letter)

        return letters

    def _extend(self, letter, row_index, col_index):
        """Return a new Sudoku puzzle obtained after one move.

        The new puzzle is identical to <self>, except that it has
        the value at position (row_index, col_index) equal to 'letter'
        instead of empty.

        'letter' must be an available letter.
        'row_index' and 'col_index' are between 0-3.

        @type self: SudokuPuzzle
        @type letter: str
        @type row_index: int
        @type col_index: int
        @rtype: SudokuPuzzle

        >>> s = SudokuPuzzle([['A', 'B', 'C', 'D'], \
                              ['C', 'D', 'A', 'B'], \
                              ['B', 'A', '', ''], \
                              ['D', 'C', '', '']])
        >>> print(s._extend('B', 2, 3))
          01|23
         ------
        0|AB|CD
        1|CD|AB
         ------
        2|BA| B
        3|DC|
        <BLANKLINE>
        """
        new_grid = [row.copy() for row in self._grid]
        new_grid[row_index][col_index] = letter
        return SudokuPuzzle(new_grid)

    def move(self, move):
        """Return a new puzzle state specified by making the given move.

        Raise a ValueError if <move> represents an invalid move.

        @type self: SudokuPuzzle
        @type move: str
        @rtype: SudokuPuzzle
        """
        # Asserts the format of the input is correct.
        try:
            # Takes move '(x, y) -> A'
            # And makes a list like so: ['(x,', 'y)', '->', 'A']
            lst = move.split()
            assert len(lst) == 4
            row_num = lst[0][1:-1]
            column_num = lst[1][0:-1]
            letter = lst[3]
            row_num = int(row_num)
            column_num = int(column_num)
        except (IndexError, AssertionError):
            raise ValueError

        if self._grid[row_num][column_num] == '' \
                and letter in self._possible_letters(row_num, column_num):

            return self._extend(letter, row_num, column_num)

        else:
            raise ValueError

    def generate_hint(self, extension):
        """Returns a possible hint for the puzzle, given extension is the next
        puzzle state.

        Precondition: extension must be in self.extensions().

        @type self: SudokuPuzzle
        @type extension: SudokuPuzzle
        @rtype: str
        >>> s = SudokuPuzzle([['', '', '', ''],\
                              ['B', 'C', 'D', 'A'],\
                              ['C', 'D', 'A', 'B'],\
                              ['A', 'B', 'C', 'D']])
        >>> t = s.extensions()[0]
        >>> print(t)
          01|23
         ------
        0|D |
        1|BC|DA
         ------
        2|CD|AB
        3|AB|CD
        <BLANKLINE>
        >>> s.generate_hint(t) # Since the two differ by D at (0, 0)
        '(0, 0) -> D'

        """
        for i in range(self._n):
            for j in range(self._n):
                if self._grid[i][j] != extension._grid[i][j]:
                    return "({}, {}) -> {}".format(i, j, extension._grid[i][j])


if __name__ == '__main__':
    import doctest
    doctest.testmod()

    # Here is a bigger Sudoku puzzle
    big = SudokuPuzzle(
        [['E', 'C', '', '', 'G', '', '', '', ''],
         ['F', '', '', 'A', 'I', 'E', '', '', ''],
         ['', 'I', 'H', '', '', '', '', 'F', ''],
         ['H', '', '', '', 'F', '', '', '', 'C'],
         ['D', '', '', 'H', '', 'C', '', '', 'A'],
         ['G', '', '', '', 'B', '', '', '', 'F'],
         ['', 'F', '', '', '', '', 'B', 'H', ''],
         ['', '', '', 'D', 'A', 'I', '', '', 'E'],
         ['', '', '', '', 'H', '', '', 'G', 'I']]
    )
    print(big)
