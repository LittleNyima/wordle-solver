class BaseWordleSolver:
    def __init__(self, dictionary):
        self.dictionary = dictionary

    def before_guess(self):
        raise NotImplementedError

    def guess(self):
        raise NotImplementedError

    def after_guess(self, result):
        raise NotImplementedError

    def reset(self):
        raise NotImplementedError