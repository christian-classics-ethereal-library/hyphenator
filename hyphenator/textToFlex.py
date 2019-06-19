#!/usr/bin/env python3
import fileinput
import sys
import yaml

from nltk.corpus import cmudict
from nltk.tokenize import SyllableTokenizer


def main(argv):
    """ WIP script to convert plain text into flextext. """
    # Make meter an inverted list of the syllable counts so "1.2.3.4" =>
    # ['4','3','2','1'].
    meter = argv[1].split('.')[::-1]
    templateFile = argv[2]
    # Read through each line: split each word into syllables
    mst = MultiSylT()
    # TODO: Come up with algorithm to pick syllable options.
    for line in fileinput.input(argv[3:]):
        length = int(meter.pop())
        line = line.replace("\n", "")
        print(syllabizeLine(line, length, mst))
    return 0


def syllabizeLine(line, n, mst):
    sentences = []
    ts = []
    words = [x for x in line.split(' ') if x != '']
    for word in words:
        ts.append(mst.multiTokenize(word))
    recurse('', ts, n, sentences)
    return sentences


def recurse(string, ts, n, sentences):
    if(n < 0 or len(ts) == 0):
        return
    for tokenization in ts[0]:
        if(len(tokenization) == n):
            sentences.append(string + ' ' + ' -- '.join(tokenization))
        elif(len(tokenization) < n):
            newstring = string + ' ' + ' -- '.join(tokenization)
            recurse(newstring, ts[1:], n - len(tokenization), sentences)


class MultiSylT(object):
    def __init__(self):
        self.SSP = SyllableTokenizer()
        with open('dict.yaml') as f:
            self.dict = yaml.safe_load(f)
        self.d = cmudict.dict()

    def multiTokenize(self, word):
        """ Return options for tokenizing a word. """
        tokenizations = []
        # If the word exists in our dictionary, return those tokenizations.
        if(word in self.dict['words']):
            tokenizations += self.dict['words'][word]

        # Otherwise, use an algorithm to get word split up into syllables
        tokenized = self.SSP.tokenize(word)
        numberOfSyllables = self.nsyl(word)

        # If the tokenized version has the same number of syllables as
        # one of the CMU STT pronunciations, return that.
        if(len(tokenized) in numberOfSyllables and tokenized not in tokenizations):
            tokenizations.append(tokenized)
        if(1 in numberOfSyllables and [word] not in tokenizations):
            tokenizations.append([word])

        # Fallback if there are no tokenizations.
        if(len(tokenizations) == 0):
            sys.stderr.write(f'{tokenized} has {len(tokenized)} syllables, '
                             + 'expected:'
                             + " or ".join(map(str, numberOfSyllables)) or "unknown")
            tokenizations.append(tokenized)
        return tokenizations

    def nsyl(self, word):
        """ Scan the CMU pronunciation dictionary to get the number of syllables
        a word should be. """
        if word in self.d:
            return [len(list(y for y in x if y[-1].isdigit()))
                    for x in self.d[word.lower()]]
        return []


if __name__ == "__main__":  # pragma: no cover
    sys.exit(main(sys.argv))
