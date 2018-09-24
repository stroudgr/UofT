# Assignment 2 - Puzzle Game
#
# CSC148 Fall 2015, University of Toronto
# Instructor: David Liu
# ---------------------------------------------
"""This module contains functions responsible for solving a puzzle.

This module can be used to take a puzzle and generate one or all
possible solutions. It can also generate hints for a puzzle (see Part 4).
"""


def solve(puzzle, verbose=False):
    """Return a solution of the puzzle.

    Even if there is only one possible solution, just return one of them.
    If there are no possible solutions, return None.

    In 'verbose' mode, print out every state explored in addition to
    the final solution. By default 'verbose' mode is disabled.

    Uses a recursive algorithm to exhaustively try all possible
    sequences of moves (using the 'extensions' method of the Puzzle
    interface) until it finds a solution.

    @type puzzle: Puzzle
    @type verbose: bool
    @rtype: Puzzle | None
    """
    if puzzle.is_solved():
        if verbose:
            print(puzzle)
        return puzzle
    else:

        for extension in puzzle.extensions():

            if solve(extension) is not None:
                if verbose and not extension.is_solved():
                    print(extension)
                return solve(extension, verbose)

        return None


def solve_complete(puzzle, verbose=False):
    """Return all solutions of the puzzle.

    Return an empty list if there are no possible solutions.

    In 'verbose' mode, print out every state explored in addition to
    the final solution. By default 'verbose' mode is disabled.

    Uses a recursive algorithm to exhaustively try all possible
    sequences of moves (using the 'extensions' method of the Puzzle
    interface) until it finds all solutions.

    @type puzzle: Puzzle
    @type verbose: bool
    @rtype: list[Puzzle]
    """

    if puzzle.is_solved():
        if verbose:
            print(puzzle)
        return [puzzle]

    lst_of_solutions = []

    for solution in puzzle.extensions():

        if verbose:
            print(solution)

        if solution.is_solved():
            lst_of_solutions.append(solution)
        else:
            if solve_complete(solution) is not []:
                lst_of_solutions += solve_complete(solution, verbose)

    return lst_of_solutions


def hint_by_depth(puzzle, n):
    """Return a hint for the given puzzle state.

    Precondition: n >= 1.

    If <puzzle> is already solved, return the string 'Already at a solution!'
    If <puzzle> cannot lead to a solution or other valid state within <n> moves,
    return the string 'No possible extensions!'

    @type puzzle: Puzzle
    @type n: int
    @rtype: str
    """
    if puzzle.is_solved():
        return "Already at a solution!"

    # Gets possible hints from helper function
    # Helper returns list of tuples (str, bool), representing moves and whether
    # they lead to a solution
    hints = possible_hints(puzzle, n)

    if len(hints) == 0:
        return "No possible extensions!"

    for hint in hints:
        # If this hint will lead to a solution, return the move.
        if hint[1]:
            return hint[0]
    # Returns a hint that may not lead to solution
    return hints[0][0]


def possible_hints(puzzle, n):
    """Returns a list tuples containing data for some extensions of puzzle:
    - the move to get to the extension
    - whether the move will lead to a solution or not

    If it finds a hint that does lead to the solution, the others become
    irrelevant, so only a returns a list containing that one hint.

    @type puzzle: Puzzle
    @type n: int
    @rtype: lst[(str, bool)]
    """

    lst = []

    extensions = puzzle.extensions()

    if n == 1:
        for extension in extensions:
            if extension.is_solved():
                return [(puzzle.generate_hint(extension), True)]
            lst.append((puzzle.generate_hint(extension), False))

    else:  # n > 1
        for extension in extensions:

            if extension.is_solved():
                return [(puzzle.generate_hint(extension), True)]

            extension_hints = possible_hints(extension, n-1)

            for hint in extension_hints:
                if hint[1]:  # if this hint will lead to a solution
                    return [(puzzle.generate_hint(extension), True)]

            # Else all the hints in extension do not lead to a solution
            # Only adds if lst is empty, since only one hint is necessary
            if len(lst) == 0 and len(extension_hints) > 0:
                lst.append((puzzle.generate_hint(extensions[0]), False))

    return lst

if __name__ == '__main__':
    from sudoku_puzzle import SudokuPuzzle
    from word_ladder_puzzle import WordLadderPuzzle
    s = SudokuPuzzle([['A', 'D', 'C', ''],
                      ['B', 'C', '', ''],
                      ['C', 'B', 'A', 'D'],
                      ['D', 'A', 'B', 'C']])
    print(s.extensions()[0])
    print('The puzzle:')
    print(s)
    print('SOLVE')
    solve(s, True)
    print('\nSOLVE-ALL')
    solve_complete(s, True)
    print('\nHINT 1')
    print(hint_by_depth(s, 1))
