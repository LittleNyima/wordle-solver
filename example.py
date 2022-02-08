from wordle import WordleDictionary, WordleProfiler, TheGreatWzkSolver

dictionary = WordleDictionary()
profiler = WordleProfiler(dictionary)
solver = TheGreatWzkSolver(dictionary)
print(profiler.evaluate_once(solver))