import os.path as osp

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

    def __iter__(self):
        return self.words.__iter__()
    
    def __len__(self):
        return self.words.__len__()

    def __getitem__(self, index):
        return self.words.__getitem__(index)
    
    def index(self, item):
        return self.words.index(item)


if __name__ == "__main__":
    import random
    dictionary = WordleDictionary()
    assert "APPLE" in dictionary
    assert "NYIMA" not in dictionary
    for _ in range(3):
        print(random.choice(dictionary))