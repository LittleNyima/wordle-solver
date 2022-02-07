import os.path as osp
import random

from ordered_set import OrderedSet

class WordleDictionary:
    def __init__(self, source=osp.join(osp.dirname(osp.realpath(__file__)), "..", "vocabulary.txt")):
        self.words = OrderedSet()
        with open(source, "r") as fin:
            lines = fin.readlines()
            for line in lines:
                self.words.add(self._validate(line.strip()))
    
    def _validate(self, word):
        assert word.isalpha(), "Parameter 'word' must consist of characters"
        assert len(word) == 5, "Parameter 'word' must consist of 5 characters"
        return word.upper()
    
    def contains(self, word):
        return word in self.words

    def choice(self):
        return random.choice(self.words)


if __name__ == "__main__":
    dictionary = WordleDictionary()
    assert dictionary.contains("APPLE")
    assert not dictionary.contains("NYIMA")
    for _ in range(3):
        print(dictionary.choice())