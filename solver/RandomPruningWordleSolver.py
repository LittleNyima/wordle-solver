import random

from wordle import WordleDictionary, WordleProfiler, BaseWordleSolver
from wordle.util import brief


class RandomPruningWordleSolver(BaseWordleSolver):
    def __init__(self, dictionary):
        super().__init__(dictionary)
        self.possible_word_list = list(dictionary)
        self.last_guess = ""

    @staticmethod
    def _stats(word):
        d = dict()
        for idx, letter in enumerate(word):
            d.setdefault(letter, [])
            d[letter].append(idx)
        return d

    def _compare(self, guess, word):
        guess_stats, word_stats = self._stats(guess), self._stats(word)
        result = [None] * 5
        for k, v in guess_stats.items():
            if k not in word_stats:
                for idx in v:
                    result[idx] = "0"
            else:
                yellows = len(word_stats[k])
                for idx in v:
                    if idx in word_stats[k]:
                        result[idx] = "2"
                        yellows -= 1
                for idx in v:
                    if idx not in word_stats[k]:
                        result[idx] = "1" if yellows > 0 else "0"
                        yellows -= 1
        return "".join(result)

    def before_guess(self):
        pass

    def guess(self):
        word = random.choice(self.possible_word_list)
        self.last_guess = word
        return word

    def after_guess(self, result):
        new_possible = []
        for word in self.possible_word_list:
            if self._compare(self.last_guess, word) == result:
                new_possible.append(word)
        self.possible_word_list = new_possible

    def reset(self):
        self.possible_word_list = list(dictionary)
        self.last_guess = ""


if __name__ == "__main__":
    dictionary = WordleDictionary()
    profiler = WordleProfiler(dictionary)
    solver = RandomPruningWordleSolver(dictionary)
    rdict = profiler.evaluate_all(solver)
    brief(rdict)
