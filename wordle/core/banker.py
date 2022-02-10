import random


class WordleGame:
    def __init__(self, dictionary):
        self.dictionary = dictionary

    def new_game(self, index=None, quiet=False):
        _secret = self.dictionary[index] if index is not None else random.choice(self.dictionary)
        return WordleGameWrapper(_secret, self.dictionary, quiet=quiet)


class WordleGameWrapper:
    def __init__(self, secret, dictionary, quiet=False):
        self._secret = secret
        self._secret_stats = self._stats(self._secret)
        self.dictionary = dictionary
        self.is_close = False
        self.quiet = quiet
        self.attempts = 0

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if exc_type:
            print("Exception occurs during the game, giving up...")
            self.give_up()
        self.is_close = True

    @staticmethod
    def _stats(word):
        d = dict()
        for idx, letter in enumerate(word):
            d.setdefault(letter, [])
            d[letter].append(idx)
        return d

    def _validate(self, word):
        assert type(word) is str, "Parameter 'word' must be string"
        assert word.isalpha(), "Parameter 'word' must consist of characters"
        assert len(word) == 5, "Parameter 'word' must consist of 5 characters"
        word = word.upper()
        assert word in self.dictionary, "`%s` is not a valid word" % word
        return word

    def _compare(self, word):
        """ 0 - secret doesn't include the character
            1 - secret includes the character, but location is not exact
            2 - secret includes the character, and location is exact
            
            Additional explanation: 
            If a character appears more times in the guess than in the answer,
            the extra occurrence will lead to a `0`.
        """
        word_stats = self._stats(word)
        result = [None] * 5
        for k, v in word_stats.items():
            if k not in self._secret_stats:
                for idx in v:
                    result[idx] = "0"
            else:
                yellows = len(self._secret_stats[k])
                for idx in v:
                    if idx in self._secret_stats[k]:
                        result[idx] = "2"
                        yellows -= 1
                for idx in v:
                    if idx not in self._secret_stats[k]:
                        result[idx] = "1" if yellows > 0 else "0"
                        yellows -= 1
        return "".join(result)

    def _print_result(self, word, result):
        print("".join(["X" if c == "0" else "O" if c == "1" else "V" for c in result]),
              "Your guess:", word)

    def guess(self, word):
        if self.is_close:
            raise ValueError("Guess operation on an exit game")
        word = self._validate(word)
        result = self._compare(word)
        self.attempts += 1
        win = result == "22222"
        if win:
            self.is_close = True
        if not self.quiet:
            self._print_result(word, result)
            if win:
                print("Succeed with %d guesses" % self.attempts)
        return result, self.attempts

    def give_up(self):
        if self.is_close:
            raise ValueError("Give up operation on an exit game, the answer is %s" % self._secret)
        if not self.quiet:
            print("Give up after %d guesses, the secret is %s" % (self.attempts, self._secret))
        self.is_close = True


if __name__ == "__main__":
    from dictionary import WordleDictionary

    dictionary = WordleDictionary()
    with WordleGame(dictionary).new_game(0) as game:
        assert game.guess("ABYSS") == ("22000", 1)
        assert game.guess("BlACk") == ("10222", 2)
        game.give_up()
    with WordleGameWrapper("SLACK", dictionary) as game:
        assert game.guess("SLASH") == ("22200", 1)
        game.give_up()
