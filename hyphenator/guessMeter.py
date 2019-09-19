#!/usr/bin/env python3
import fileinput
import re
import sys

import hyphenator.textToFlex as ttf
from hyphenator import wordSyl


def main(argv):
    """ For a paragraph of text, will guess the syllables in each line,
    separated by a period, like "8.6.8.6".
    """
    lines = ""
    mst = ttf.MultiSylT(lang=argv[1])
    for line in fileinput.input(argv[2:]):
        if line.strip() != '':
            lines = lines + line
        elif lines.strip():
            print(guessMeter(lines.strip(), argv[1], mst))
            lines = ''
    if lines.strip():
        print(guessMeter(lines.strip(), argv[1], mst))


def guessMeter(paragraph, lang, mst=None):
    meter = ''
    if mst is None:
        mst = ttf.MultiSylT(lang=lang)
    for line in paragraph.split("\n"):
        count = 0
        words = [x.strip() for x in line.split(' ') if x.strip() != '']
        for word in words:
            if word.strip(wordSyl.puncs) != '':
                # Assuming the first word from the multiTokenizer is the best!
                count += len(mst.multiTokenize(word)[0])
        meter = meter + str(count) + "."
    return meter.strip('.')


if __name__ == "__main__":  # pragma: no cover
    sys.exit(main(sys.argv))
