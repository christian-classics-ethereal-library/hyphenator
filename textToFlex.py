#!/usr/bin/env python3
import fileinput
import sys
import yaml

from nltk.tokenize import SyllableTokenizer


def main(argv):
    """ WIP script to convert plain text into flextext. """
    meter = argv[1]
    templateFile = argv[2]
    # Read through each line: split each word into syllables
    mst = MultiSylT()
    # TODO: Come up with algorithm to pick syllable options.
    for line in fileinput.input(argv[3:]):
        line = line.replace("\n", "")
        words = [x for x in line.split(' ') if x != '']
        for word in words:
            sys.stdout.write(' -- '.join(mst.multiTokenize(word)[0]) + " ")
    return 0


class MultiSylT(object):
    def __init__(self):
        self.SSP = SyllableTokenizer()
        with open('dict.yaml') as f:
            self.dict = yaml.safe_load(f)

    def multiTokenize(self, word):
        """ Return options for tokenizing a word. """
        if(word in self.dict['words']):
            return self.dict['words'][word]
        return [self.SSP.tokenize(word)]


if __name__ == "__main__":
    sys.exit(main(sys.argv))
