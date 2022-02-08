# Wordle Solver

Implementation of [Wordle - A daily word game (powerlanguage.co.uk)](https://www.powerlanguage.co.uk/wordle/) game and a framework of evaluating Wordle solvers.

## Examples

- You can play the game manually:

  ```python
  from wordle import WordleGame, WordleDictionary
  
  with WordleGame(WordleDictionary()).new_game() as game:
      res, attempts = "00000", 0
      while not res == "22222":
          guess = input("Please make your guess: ").strip()
          res, attempts = game.guess(guess)
  ```

- You can implement your own solver and evaluate it using profiler:

  ```python
  import random
  from wordle import WordleDictionary, WordleProfiler, BaseWordleSolver
  
  class RandomWordleSolver(BaseWordleSolver):
      def __init__(self, dictionary):
          super().__init__(dictionary)
      def before_guess(self):
          pass
      def guess(self):
          return random.choice(self.dictionary)
      def after_guess(self, result):
          pass
  
  dictionary = WordleDictionary()
  profiler = WordleProfiler(dictionary)
  solver = RandomWordleSolver(dictionary)
  print(profiler.evaluate_once(solver))
  ```

## Contribution

Welcome to create pull requests and contribute your own solver!

