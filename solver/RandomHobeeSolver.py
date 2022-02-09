import random

from wordle import WordleDictionary, WordleProfiler, BaseWordleSolver
from wordle.util import stats


class RandomHobeeSolver(BaseWordleSolver):
    def __init__(self, dictionary):
        super().__init__(dictionary)

    def before_guess(self):
        pass

    def guess(self):
        return random.choice(self.dictionary)

    def after_guess(self, result):
        pass

    def reset(self):
        pass


if __name__ == "__main__":
    dictionary = WordleDictionary()
    profiler = WordleProfiler(dictionary)
    solver = RandomHobeeSolver(dictionary)
    print(profiler.evaluate_once(solver, index=dictionary.words.index("SADLY")))
    # print(profiler.evaluate_all(solver))
    rdict = profiler.evaluate_all(solver)
    stats.brief(rdict)
