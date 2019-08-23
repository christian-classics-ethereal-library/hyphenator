#!/usr/bin/env python3
import fileinput
import json
import os.path
import pyphen
import re
import sys
import yaml

from nltk.corpus import cmudict
from nltk.tokenize import SyllableTokenizer

from hyphenator import wordSyl


def main(argv):
    """ Script to convert plain text into flextext.
    argv[1] is the meter, like 8.6.8.6.
    argv[2] is the file to use as a template, or '-' for no file.
    argv[3] is the dictionary of hyphenations.
    argv[4] is the two-letter language code, or '-' for undetermined.
    additional arguments are used as input if they are present
    the flextext is sent to stdout
    stderr is a YAML document including warnings and alternate verses
    """
    if(len(argv) < 2):
        error("Usage %s" % main.__doc__)
        return
    # Make meter an inverted list of the syllable counts so "1.2.3.4" =>
    # ['4','3','2','1'].
    meter = argv[1].split('.')[::-1]
    templateFile = argv[2] if len(argv) > 2 else '-'
    mst = MultiSylT(argv[3] if len(argv) > 3 else '-', argv[4] if len(argv) > 4 else 'en')
    success = True
    i = 0
    for line in fileinput.input(argv[5:]):
        i += 1
        try:
            length = int(meter.pop())
        except BaseException:
            error("Out of lines in meter.")
            return
        line = line.replace("\n", "")
        syllabized = syllabizeLine(line, length, mst)
        if(syllabized):
            print(syllabized[0])
            if(len(syllabized) > 1):
                message('alternates', i)
                messageData('data', syllabized)
        else:
            success = False
            print('')
            error("Unable to syllabize '%s' to %d syllables" % (line, length))
    return 0 if success else 1


def syllabizeLine(line, n, mst, lang=None):
    if lang != mst.lang:
        mst.changeLang(lang)
    sentences = []
    ts = []
    words = [x for x in line.split(' ') if x != '']
    for word in words:
        if(word.strip(wordSyl.puncs) == ''):
            warning("Word '%s' consists only of punctuation" % word)
        else:
            ts.append(mst.multiTokenize(word))
    recurse('', ts, n, sentences)
    return sentences


def recurse(string, ts, n, sentences):
    if(n < 0 or len(ts) == 0):
        return
    for tokenization in ts[0]:
        if(len(tokenization) == n and len(ts) == 1):
            sentences.append(string + ' -- '.join(tokenization))
        elif(len(tokenization) < n):
            newstring = string + ' -- '.join(tokenization) + ' '
            recurse(newstring, ts[1:], n - len(tokenization), sentences)


def message(key, msg):
    """Write a message as a yaml object item of an array."""
    sys.stderr.write("- " + key + ": " + json.dumps(msg) + "\n")


def messageData(key, data):
    """Write additional attributes into the last message object."""
    sys.stderr.write("  " + key + ": " + json.dumps(data) + "\n")


def error(msg):
    message('error', msg)


def warning(msg):
    message('warning', msg)


class MultiSylT(object):
    def __init__(self, dictName, lang=None):
        # Sonority Sequencing Tokenizer is currently only set up for 26 latin letters,
        # english pronunciation.
        self.SSP = SyllableTokenizer()
        self.changeLang(lang)
        self.dict = {"words": []}
        if (dictName == '-'):
            dictName = os.path.dirname(__file__) + "/dict.yaml"
        try:
            with open(dictName) as f:
                self.dict = yaml.safe_load(f)
        except BaseException:
            error("%s could not be loaded." % dictName)
        # CMU Pronunciation dictionary includes 119K+ words of different languages,
        # using the latin alphabet, occasionally with punctuation.
        self.d = cmudict.dict()

    def changeLang(self, lang):
        if lang not in pyphen.LANGUAGES:
            lang = 'en'
        self.pyphen = pyphen.Pyphen(lang=lang)
        self.lang = lang

    def multiTokenize(self, originalWord):
        """ Return options for tokenizing a word. """
        word = self.deformat(originalWord)
        tokenizations = []
        # If the word exists in our dictionary, include those tokenizations.
        if(word in self.dict['words']):
            tokenizations += self.dict['words'][word]

        # Otherwise, use an algorithm to get word split up into syllables
        tokenized = self.SSP.tokenize(word)
        sylCounts = self.nsyl(word)
        splitter = "\t"
        hyphenated = self.pyphen.inserted(word, splitter).split(splitter)

        # If the tokenized or hyphenated version has the same number of
        # syllables as one of the CMU STT pronunciations, but we don't
        # already have that syllable-count represented, include it.
        lh = len(hyphenated)
        if(lh in sylCounts and lh not in map(len, tokenizations)):
            tokenizations.append(hyphenated)
        lt = len(tokenized)
        if(lt in sylCounts and lt not in map(len, tokenizations)):
            tokenizations.append(tokenized)

        if(1 in sylCounts and [word] not in tokenizations):
            tokenizations.append([word])

        # Fallback if there are no tokenizations.
        if(len(tokenizations) == 0):
            warning("%s has %d syllables," % (str(hyphenated), len(hyphenated))
                    + ' expected: '
                    + (" or ".join(map(str, sylCounts)) or "???")
                    )
            tokenizations.append(hyphenated)
        return list(map(self.reformat, tokenizations, [
                    originalWord for x in range(0, len(tokenizations))]))

    def deformat(self, word):
        return word.lower().strip(wordSyl.puncs)

    def reformat(self, oldTokenized, template):
        # Since tokenized is mutable, create a duplicate of it.
        tokenized = list(oldTokenized)
        plainTemp = template.strip(wordSyl.puncs)
        if(plainTemp and plainTemp.isupper()):
            tokenized[0] = tokenized[0].upper()
        elif(plainTemp and plainTemp[0].isupper()):
            tokenized[0] = tokenized[0][0].upper() + tokenized[0][1:]
        match = re.search(r"^[" + wordSyl.puncs + r"]+", template)
        starting = match.group(0) if match else ''
        match = re.search(r"[" + wordSyl.puncs + r"]+$", template)
        ending = match.group(0) if match else ''
        tokenized[0] = starting + tokenized[0]
        tokenized[-1] = tokenized[-1] + ending
        return tokenized

    def nsyl(self, word):
        """Get the number of syllables a word should be
        from the CMU Pronunciation dictionary.
        Returned as a list to account for variants."""
        if word in self.d:
            return [len(list(y for y in x if y[-1].isdigit()))
                    for x in self.d[word.lower()]]
        return []


if __name__ == "__main__":  # pragma: no cover
    sys.exit(main(sys.argv))
