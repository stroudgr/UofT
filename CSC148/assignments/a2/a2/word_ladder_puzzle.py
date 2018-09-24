# Assignment 2 - Puzzle Game
#
# CSC148 Fall 2015, University of Toronto
# Instructor: David Liu
# ---------------------------------------------
"""Word ladder module.

Your task is to complete the implementation of this class so that
you can use it to play Word Ladder in your game program.

Rules of Word Ladder
--------------------
1. You are given a start word and a target word (all words in this puzzle
   are lowercase).
2. Your goal is to reach the target word by making a series of *legal moves*,
   beginning from the start word.
3. A legal move at the current word is to change ONE letter to get
   a current new word, where the new word must be a valid English word.

The sequence of words from the start to the target is called
a "word ladder," hence the name of the puzzle.

Example:
    Start word: 'make'
    Target word: 'cure'
    Solution:
        make
        bake
        bare
        care
        cure

    Note that there are many possible solutions, and in fact a shorter one
    exists for the above puzzle. Do you see it?

Implementation details:
- We have provided some starter code in the constructor which reads in a list
  of valid English words from wordsEn.txt. You should use this list to
  determine what moves are valid.
- **WARNING**: unlike Sudoku, Word Ladder has the possibility of getting
  into infinite recursion if you aren't careful. The puzzle state
  should keep track not just of the current word, but all words
  in the ladder. This way, in the 'extensions' method you can just
  return the possible new words which haven't already been used.
"""
from puzzle import Puzzle


CHARS = 'abcdefghijklmnopqrstuvwxyz'


class WordLadderPuzzle(Puzzle):
    """A word ladder puzzle."""
    # === Private attributes ===
    # @type _words: list[str]
    #     List of allowed English words
    # @type _start: str
    #     The word the player is at now
    # @type _target: str
    #     The word the player is trying to guess
    # @type _previous_words: lst[str]
    #     A list of words the player has already used, including <_start>.

    def __init__(self, start, target, used_words=[]):
        """Create a new word ladder puzzle with given start and target words.

        @type self: WordLadderPuzzle
        @type start: str
        @type target: str
        @rtype: None
        """
        # Code to initialize _words.
        self._words = []
        with open('wordsEn.txt') as wordfile:
            for line in wordfile:
                self._words.append(line.strip())

        self._start = start
        self._target = target
        self._previous_words = used_words + [start]

    def __str__(self):
        """Return a human-readable representation of this puzzle.

        @type self: WordLadderPuzzle
        @rtype: str
        """
        return " ]|||[ ".join(map(str, self._previous_words))

    def is_solved(self):
        """Return whether this puzzle is in a solved state.

        @type self: WordLadderPuzzle
        @rtype: bool
        """
        return self._start == self._target

    def extensions(self):
        """Return a list of possible new states after a valid move.

        The valid move must change exactly one character of the
        current word, and must result in an English word stored in
        self._words.

        You should *not* perform any moves which produce a word
        that is already in the ladder.

        The returned moves should be sorted in alphabetical order
        of the produced word.

        @type self: WordLadderPuzzle
        @rtype: list[WordLadderPuzzle]
        """
        extensions = []

        # Go through every character in the alphabet
        for char in CHARS:

            start = self._start

            for i in range(len(start)):
                # Replace one of the letters in the word with another one.
                new_word = start[:i] + char + start[i+1:]

                # Checks if this is a valid word.
                if new_word in self._words \
                        and new_word not in self._previous_words:

                    extent = WordLadderPuzzle(new_word,
                                              self._target,
                                              self._previous_words)

                    # Adds extension to list of extensions, ensuring
                    # alphabetical order.
                    for index in range(len(extensions)):
                        if extensions[index]._start > extent._start:
                            extensions.insert(index, extent)
                            break
                    if extent not in extensions:
                        extensions.append(extent)

        return extensions

    def move(self, move):
        """Return a new puzzle state specified by making the given move.
        This method is non-mutating.
        Raise a ValueError if <move> represents an invalid move.

        @type self: WordLadderPuzzle
        @type move: str
        @rtype: WordLadderPuzzle
        """

        # Checks if the word has been used, then if it can be used, then if it
        # is an actual word in the dictionary.
        if move in self._previous_words or not similar(self._start, move) \
                or move not in self._words:

            raise ValueError

        else:
            return WordLadderPuzzle(move, self._target, self._previous_words)

    def generate_hint(self, extension):
        """Returns a possible hint for the puzzle, given extension is the next
        puzzle state.

       Precondition: extension must be in self.extensions().

        @type self: WordLadderPuzzle
        @type extension: WordLadderPuzzle
        @rtype: str
        """
        return extension._start


# -------------------------------------------------------
# Helper function for move method in WordLadderPuzzle
# -------------------------------------------------------


def similar(word1, word2):
    """Returns whether two words are the same, or off by one letter.
    @type word1: str
    @type word2: str
    @rtype: bool
    >>> similar('sake', 'cake')
    True
    >>> similar('snake', 'cake')
    False
    >>> similar('cake', 'cats')
    False
    """

    if len(word1) != len(word2):
        return False
    else:
        are_equal = True
        for i in range(len(word1)):
            if are_equal and word1[i] != word2[i]:
                are_equal = False
            elif word1[i] != word2[i]:
                return False

        return True

if __name__ == '__main__':
    import doctest
