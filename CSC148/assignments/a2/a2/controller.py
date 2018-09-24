# Assignment 2 - Puzzle Game
#
# CSC148 Fall 2015, University of Toronto
# Instructor: David Liu
# ---------------------------------------------
"""Module containing the Controller class."""
from view import TextView, WebView
from puzzle import Puzzle
from solver import solve, solve_complete, hint_by_depth


class Controller:
    """Class responsible for connection between puzzles and views.

    You may add new *private* attributes to this class to help you
    in your implementation.
    """
    # === Private Attributes ===
    # @type _puzzle: Puzzle
    #     The puzzle associated with this game controller
    # @type _view: View
    #     The view associated with this game controller
    # @type _state_tree: Tree
    #     A Tree representation of the current puzzle state and the move to get
    #     to it, with ancestors and descendants serving as references to
    #     previous and attempted states.
    def __init__(self, puzzle, mode='text'):
        """Create a new controller.

        <mode> is either 'text' or 'web', representing the type of view
        to use.

        By default, <mode> has a value of 'text'.

        @type puzzle: Puzzle
        @type mode: str
        @rtype: None
        """
        self._puzzle = puzzle
        if mode == 'text':
            self._view = TextView(self)
        elif mode == 'web':
            self._view = WebView(self)
        else:
            raise ValueError()

        self._state_tree = Tree(self._puzzle)

        # Start the game.
        self._view.run()

    def state(self):
        """Return a string representation of the current puzzle state.

        @type self: Controller
        @rtype: str
        """
        return str(self._puzzle)

    def act(self, action):
        """Run an action represented by string <action>.

        Return a string representing either the new state or an error message,
        and whether the program should end.

        @type self: Controller
        @type action: str
        @rtype: (str, bool)
        """

        if action == 'exit':
            return '', True

        elif action == ':SOLVE':
            return solve(self._puzzle).__str__(), True

        elif action == ':SOLVE-ALL':
            return "\n".join(map(str, solve_complete(self._puzzle))), True

        # The remaining conditions use helpers for more complicated code.
        elif action == ':UNDO':
            return self._undo(), False

        elif action == ':ATTEMPTS':
            return self._state_tree.attempts(), False

        elif action[:6] == ":HINT ":
            return self._hint(action), False

        elif isinstance(action, str):
            # The action is some sort of move that depends on the puzzle.
            # rtype of _player_move is (str, bool), since a move could cause the
            # game to end.
            return self._player_move(action)

        # Nothing happens if input is somehow incorrect.
        else:
            return self.state(), False

    # ------------------------------------------------------------------------
    # Helpers for method 'act'
    # ------------------------------------------------------------------------

    def _undo(self):
        """Returns a string representation of the puzzle state that the player
        had before the current state.

        Returns "You can no longer undo" if the player has reached the initial
        puzzle state.

        @type self: Controller
        @rtype: str
        """
        # Find the previous puzzle state as a Tree
        previous_puzzle_tree = self._state_tree.undo()

        if previous_puzzle_tree is None:
            return "You can no longer undo"
        else:
            # Sets current puzzle state to the previous state
            self._puzzle = previous_puzzle_tree._state
            self._state_tree = previous_puzzle_tree
            return self._puzzle.__str__()

    def _hint(self, action):
        """Returns a hint based on the players action

        Precondition: action must be in the following format: ':HINT n'
         where n is an integer.

        @type self: Controller
        @type action: str
        @rtype: str
        """
        try:
            number = action[6:]
            number = int(number)
        except ValueError:
            return "That is not a proper value. Try again."

        return hint_by_depth(self._puzzle, number)

    def _player_move(self, action):
        """Changes current puzzle state to one according to <action>.
        Returns a string representation of the game, as well as whether the
        program should end.

         @type self: Controller
         @type action: str
         @rtype: (str, bool)
         """
        try:
            state = self._puzzle.move(action)
        except ValueError:
            return "This is not a valid input.", False

        self._state_tree = self._state_tree.add_state(state, action)
        self._puzzle = state
        if self._puzzle.is_solved():
            return self._puzzle.__str__() + "\nCongratulations! You've " \
                                                "solved the Puzzle!", True
        else:
            return self._puzzle.__str__(), False


class Tree:
    """
    A Tree class specifically for keeping track of Puzzle states.
    """
    # === Private Attributes ===
    # @type _state: Puzzle
    #     The state of the puzzle.
    # @type _move: move
    #     The move that the player made to get to _state.
    # @type _subtrees: list[Tree]
    #     The moves that a player has made afterwards, i.e. the tree's children.
    # @type _previous: Tree | None
    #     The parent of the tree, representing the previous state.

    def __init__(self, state, move='', previous=None):
        """
        @type self: Tree
        @type state: Puzzle
        @type move: str
        @type previous: Tree | None
        @rtype: None
        """
        self._state = state
        self._move = move
        self._subtrees = []
        self._previous = previous

    def add_state(self, state, move):
        """Adds and returns a new subtree to the Tree based on <state> and
        <move>, or returns the subtree that is already initialized to this in
        the Tree.

        @type self: Tree
        @type state: Puzzle
        @type move: str
        @rtype: Tree
        """
        for subtree in self._subtrees:
            if subtree._move == move:
                return subtree

        t = Tree(state, move, self)
        self._subtrees.append(t)
        return t

    def undo(self):
        """Returns previous state of Tree (the parent of <self>).

        @type self: Tree
        @rtype: Tree
        """
        return self._previous

    def attempts(self):
        """Returns all the states of the children, i.e. whatever moves someone
        has attempted.

        @type self: Tree
        @rtype: str
        """
        if len(self._subtrees) == 0:
            return "You have not attempted anything yet."

        result = ''

        for tree in self._subtrees:
            result += "\n> " + tree._move + "\n" + tree._state.__str__()

        return result + '\n'


if __name__ == '__main__':
    from sudoku_puzzle import SudokuPuzzle
    from word_ladder_puzzle import WordLadderPuzzle

    s = SudokuPuzzle([['', '', '', ''],
                      ['', '', '', ''],
                      ['C', 'D', 'A', 'B'],
                      ['A', 'B', 'C', 'D']])

    c = Controller(s, 'text')
