from wordle import WordleDictionary, WordleProfiler, BaseWordleSolver
from wordle.util import stats


class TheGreatWzkSolver(BaseWordleSolver):
    def __init__(self, dictionary, verbose=True):
        self.dictionary = [ch.lower() for ch in dictionary]
        self.verbose = verbose
        # a very long line, to examine how wide your monitor is
        self.freq = [
            {'a': 141, 'b': 173, 'c': 198, 'd': 111, 'e': 71, 'f': 136, 'g': 115, 'h': 69, 'i': 34, 'j': 20, 'k': 20,
             'l': 88, 'm': 107, 'n': 37, 'o': 41, 'p': 142, 'q': 23, 'r': 105, 's': 366, 't': 149, 'u': 33, 'v': 43,
             'w': 83, 'x': 0, 'y': 6, 'z': 3},
            {'a': 304, 'b': 16, 'c': 40, 'd': 20, 'e': 242, 'f': 8, 'g': 12, 'h': 144, 'i': 202, 'j': 2, 'k': 10,
             'l': 201, 'm': 38, 'n': 86, 'o': 279, 'p': 61, 'q': 5, 'r': 267, 's': 16, 't': 77, 'u': 186, 'v': 15,
             'w': 44, 'x': 14, 'y': 23, 'z': 2},
            {'a': 306, 'b': 57, 'c': 56, 'd': 75, 'e': 177, 'f': 25, 'g': 67, 'h': 9, 'i': 266, 'j': 3, 'k': 12,
             'l': 112, 'm': 61, 'n': 139, 'o': 244, 'p': 58, 'q': 1, 'r': 163, 's': 80, 't': 111, 'u': 165, 'v': 49,
             'w': 26, 'x': 12, 'y': 29, 'z': 11},
            {'a': 163, 'b': 24, 'c': 151, 'd': 69, 'e': 318, 'f': 35, 'g': 76, 'h': 28, 'i': 158, 'j': 2, 'k': 55,
             'l': 162, 'm': 68, 'n': 182, 'o': 132, 'p': 50, 'q': 0, 'r': 152, 's': 171, 't': 139, 'u': 82, 'v': 46,
             'w': 25, 'x': 3, 'y': 3, 'z': 20},
            {'a': 64, 'b': 11, 'c': 31, 'd': 118, 'e': 424, 'f': 26, 'g': 41, 'h': 139, 'i': 11, 'j': 0, 'k': 113,
             'l': 156, 'm': 42, 'n': 130, 'o': 58, 'p': 56, 'q': 0, 'r': 212, 's': 36, 't': 252, 'u': 1, 'v': 0,
             'w': 17, 'x': 8, 'y': 364, 'z': 4}]
        self.yellows = []
        self.greens = []
        self.blacks = set()
        self.attempts = []
        self.prev_guess = None

    def words_like(self, query, excluded=()):
        assert len(query) == 5
        condition = [0, 0, 0, 0, 0]
        for i, ch in enumerate(query):
            if ch.isalpha():
                condition[i] = ch.lower()

        ans = []
        for word in self.dictionary:
            flag = False
            for exclu in excluded:
                if exclu in word:
                    flag = True
                    break
            if flag:
                continue
            for i, cond in enumerate(condition):
                if cond != 0 and cond != word[i]:
                    flag = True
                    break
            if not flag:
                ans.append(word)
        return ans

    def possible_words(self, yellows=(), greens=(), blacks=()):
        g, y = greens.copy(), yellows.copy()
        for i, green in enumerate(greens):
            g[i] = (green[0].lower(), int(green[1]) - 1)
        for i, yellow in enumerate(yellows):
            y[i] = (yellow[0].lower(), int(yellow[1]) - 1)

        query = ["-"] * 5
        for ch, pos in g:
            query[pos] = ch

        possible_words = self.words_like(query, [b.lower() for b in blacks])
        ans = []
        for word in possible_words:
            flag = False
            for ch, pos in y:
                if ch not in word or word[pos] == ch:
                    flag = True
                    break
            if not flag:
                ans.append(word)
        return ans

    def before_guess(self):
        if self.verbose:
            print("The great WZK is guessing your stupid word!!!")

    def guess(self):
        words = self.possible_words(self.yellows, self.greens, self.blacks)
        if len(words) < 10 and self.verbose:
            print("possible words:", words)

        best = 0
        best_word = "NONE"
        for word in words:
            if word in self.attempts:
                continue
            cnt = 0
            for i, ch in enumerate(word):
                cnt += self.freq[i][ch]
            if cnt > best:
                best = cnt
                best_word = word

        if best_word == "NONE":
            raise ValueError("No possible candidate words. Blame LittleNyima for his banker and profiler!")
        self.prev_guess = best_word
        if self.verbose:
            print("I guess: ", best_word)
        return best_word

    def after_guess(self, result):
        if result == '22222':
            if self.verbose:
                print("I AM A GENIUS")
        else:
            if self.verbose:
                print("I don't believe it! How can I be wrong???")
            # import os
            # os.system('shutdown')

        self.attempts.append(self.prev_guess)

        seen_chars = set()
        for i, ch in enumerate(result):
            if ch == "2":
                self.greens.append(self.prev_guess[i] + str(i + 1))
                seen_chars.add(self.prev_guess[
                                   i])  # TODO: uncomment this if result calculation (when duplicated chars exists) is changed

        for i, ch in enumerate(result):
            if ch == "1":
                self.yellows.append(self.prev_guess[i] + str(i + 1))
                seen_chars.add(self.prev_guess[
                                   i])  # TODO: uncomment this if result calculation (when duplicated chars exists) is changed
            elif ch == "0" and self.prev_guess[i] not in seen_chars:
                self.blacks.add(self.prev_guess[i])

    def reset(self):
        self.yellows = []
        self.greens = []
        self.blacks = set()
        self.attempts = []
        self.prev_guess = None


if __name__ == "__main__":
    dictionary = WordleDictionary()
    profiler = WordleProfiler(dictionary)
    solver = TheGreatWzkSolver(dictionary, verbose=True)
    print(profiler.evaluate_once(solver, index=dictionary.words.index("SADLY")))
    # print(profiler.evaluate_all(solver))
    rdict = profiler.evaluate_all(solver)
    stats.brief(rdict)
