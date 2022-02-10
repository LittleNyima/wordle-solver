import random

from wordle import WordleDictionary, WordleProfiler, BaseWordleSolver
from wordle.util import stats


class RandomHobeeSolver(BaseWordleSolver):
    def __init__(self, dic):
        super().__init__(dic)
        self.last_guess = None
        self.last_result = None
        self.possible_dictionary = self.dictionary
        self.dictionary_index = None
        self.first_guess = True

    def is_possible(self, word):
        for i, v in enumerate(word):
            if self.last_guess[i] == v and self.last_result[i] == "1":
                return False
            elif self.last_guess[i] != v and self.last_result[i] == "2":
                return False

        must_include = []
        for i, v in enumerate(self.last_result):
            if v == "1":
                must_include.append(self.last_guess[i])
        for i in must_include:
            if i not in word:
                return False

        b, y, g = [], [], []
        for i, v in enumerate(self.last_result):
            if v == "0":
                b.append(self.last_guess[i])
            elif v == "1":
                y.append(self.last_guess[i])
            else:
                g.append(self.last_guess[i])
        must_exclude = []
        for v in b:
            if v not in y and v not in g:
                must_exclude.append(v)
        for i in must_exclude:
            if i in word:
                return False

        return True

    def before_guess(self):
        # build dictionary index
        pass

    def guess(self):
        if self.first_guess:
            self.first_guess = False
            first_guess_possible_dictionary = []
            for i in self.possible_dictionary:
                if len(set(i)) == 5:
                    first_guess_possible_dictionary.append(i)
            self.last_guess = random.choice(first_guess_possible_dictionary)
        else:
            self.last_guess = random.choices(self.possible_dictionary, k=1)[0]
        return self.last_guess

    def after_guess(self, result):
        self.last_result = result
        new_possible_dictionary = []
        for i in self.possible_dictionary:
            if self.is_possible(i):
                new_possible_dictionary.append(i)
        if len(new_possible_dictionary) != 0:
            self.possible_dictionary = new_possible_dictionary

    def reset(self):
        self.__init__(self.dictionary)


if __name__ == "__main__":
    dictionary = WordleDictionary()
    profiler = WordleProfiler(dictionary)
    solver = RandomHobeeSolver(dictionary)
    print(profiler.evaluate_once(solver, index=dictionary.words.index("SADLY")))
    rdict = profiler.evaluate_all(solver)
    stats.brief(rdict)
