# game.py
# pylint: disable=missing-docstring
# pylint: disable=too-few-public-methods

import random
import string

class Game:

    def __init__(self):
        self.grid = random.choices(string.ascii_uppercase, k=9)

    def is_valid(self, word):
        if not word:
            return False
        copy = self.grid.copy()
        for char in word:
            if char not in copy:
                return False
            copy.remove(char)
        return True
