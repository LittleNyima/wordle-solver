import time
import traceback

from .banker import WordleGame


class WordleProfiler:
    def __init__(self, dictionary, max_attempts=6):
        self.dictionary = dictionary
        self.banker = WordleGame(dictionary)
        self.record = dict()
        self.max_attempts = max_attempts

    def _evaluate_once(self, solver, index):
        with self.banker.new_game(index) as game:
            result, tries, initial, clock_time = "", 0, True, 0
            while result != "22222" and tries < self.max_attempts:
                try:
                    if initial:
                        solver.reset()
                        initial = False
                    tik = time.process_time()
                    solver.before_guess()
                    guess = solver.guess()
                    result, tries = game.guess(guess)
                    solver.after_guess(result)
                    tok = time.process_time()
                    clock_time += tok - tik
                except KeyboardInterrupt as e:
                    raise e
                except:
                    traceback.print_exc()
                    print("Exception occurs during the game, giving up...")
                    break
            if result != "22222":
                tries = self.max_attempts + 1
                game.give_up()
        return tries, clock_time

    def evaluate_once(self, solver, index=None):
        return self._evaluate_once(solver, index)

    def evaluate_all(self, solver):
        r = {"words": {}, "time_cost": 0, "meta": {}}
        r["meta"] = {
            "solver": solver.__class__.__name__,
            "max_attempts": self.max_attempts
        }
        self.record[solver.__class__.__name__] = r
        for idx, word in enumerate(self.dictionary):
            tries, clock_time = self._evaluate_once(solver, idx)
            r["words"][word] = tries
            r["time_cost"] += clock_time
        return r
