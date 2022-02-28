import math

from wordle import WordleDictionary, WordleProfiler, BaseWordleSolver
from wordle.util import brief
from tqdm import tqdm

class MaxEntropySolver(BaseWordleSolver):
    def __init__(self, dictionary):
        super().__init__(dictionary)
        self.initial = True
        self.possibility_cache = dict()
        self.possible_word_set = set(self.dictionary)
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
    
    def cache_possibilities(self):
        for guess in tqdm(self.dictionary):
            mapping = dict()
            for answer in self.dictionary:
                result = self._compare(guess, answer)
                mapping.setdefault(result, set())
                mapping[result].add(answer)
            self.possibility_cache[guess] = mapping
    
    def before_guess(self):
        if self.initial:
            self.cache_possibilities()
            self.initial = False
    
    def guess(self):
        max_entropy, max_word = 0.0, ""
        for guess in self.possible_word_set:
            entropy = 0.0
            for _, v in self.possibility_cache[guess].items():
                possible_words = v & self.possible_word_set
                if possible_words:
                    p = len(possible_words) / len(self.possible_word_set)
                    entropy -= p * math.log2(p)
            if math.isclose(entropy, 0.0):
                self.last_guess = guess
                return guess
            if entropy > max_entropy:
                max_entropy, max_word = entropy, guess
        self.last_guess = max_word
        return max_word

    def after_guess(self, result):
        self.possible_word_set = self.possibility_cache[self.last_guess][result] & self.possible_word_set

    def reset(self):
        self.possible_word_set = set(self.dictionary)
        self.last_guess = ""


if __name__ == "__main__":
    dictionary = WordleDictionary()
    profiler = WordleProfiler(dictionary)
    solver = MaxEntropySolver(dictionary)
    rdict = profiler.evaluate_all(solver)
    brief(rdict)
