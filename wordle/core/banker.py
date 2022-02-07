class WordleGame:
    def __init__(self, dictionary):
        self.dictionary = dictionary
    
    def new_game(self, quiet=False):
        return WordleGameWrapper(self.dictionary.choice(), self.dictionary,
                                 quiet=quiet)

class WordleGameWrapper:
    def __init__(self, secret, dictionary, quiet=False):
        self._secret = secret
        self.dictionary = dictionary
        self.is_close = False
        self.quiet = quiet
        self.attempts = 0

    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_value, traceback):
        self.is_close = True

    def _validate(self, word):
        assert type(word) is str, "Parameter 'word' must be string"
        assert word.isalpha(), "Parameter 'word' must consist of characters"
        assert len(word) == 5, "Parameter 'word' must consist of 5 characters"
        assert self.dictionary.contains(word), "`%s` is not a valid word" % word
        return word.upper()
    
    def _compare(self, word):
        """ 0 - secret doesn't include the character
            1 - secret includes the character, but location is not exact
            2 - secret includes the character, and location is exact
        """
        return "".join(["0" if c not in self._secret else
                        "1" if c != self._secret[idx] else
                        "2" for idx, c in enumerate(word)])

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
        if not self.quiet:
            print("Give up after %d guesses, the secret is %s" % (self.attempts, self._secret))
        self.is_close = True


if __name__ == "__main__":
    from dictionary import WordleDictionary
    dictionary = WordleDictionary()
    with WordleGame(dictionary).new_game() as game:
        game.guess("APPLE")
        game.guess("YIELD")
        game.guess("BROOK")
        game.give_up()