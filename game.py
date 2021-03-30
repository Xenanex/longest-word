# game.py
# pylint: disable=missing-docstring
# pylint: disable=too-few-public-methods

import random
import string
import requests

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
        return self.__check_API(word)

    @staticmethod
    def __check_API(word):
        r = requests.get(f"https://wagon-dictionary.herokuapp.com/{word}")
        # Response possible:
        #   - Not exist: {"found":false,"word":"gikdfofgda","error":"word not found"}
        #   - Exist: {"found":true,"word":"test","length":4}
        if r.status_code != 200:
            raise RuntimeError("Trouble with the verification API")
        body = r.json()
        return body.get("found")
