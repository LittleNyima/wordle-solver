from .banker import WordleGame

class WordleProfiler:
    def __init__(self, dictionary, max_attempts=6):
        self.dictionary = dictionary
        self.banker = WordleGame(dictionary)
        self.record = dict()
        self.max_attempts = max_attempts

    def _evaluate_once(self, solver, index):
        with self.banker.new_game(index) as game:
            result, tries = "", 0
            while result != "22222" and tries <= self.max_attempts:
                solver.before_guess()
                guess = solver.guess()
                result, tries = game.guess(guess)
                solver.after_guess(result)
            if result != "22222":
                game.give_up()
        return tries

    def evaluate_once(self, solver):
        return self._evaluate_once(solver, None)

    def evaluate_all(self, solver):
        r = dict()
        self.record[solver.__class__.__name__] = r
        for idx, word in enumerate(self.dictionary):
            r[word] = self._evaluate_once(solver, idx)
        return r