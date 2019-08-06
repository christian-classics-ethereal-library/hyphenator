#!/usr/bin/env python3
import fileinput
import re
import sys

puncs = r",.:;!?\*()_"
# Include the backslash before the hyphen so it doesn't break regexes.
puncs += r"\-"
# Smart double-quotes
puncs += "\u201c\u201d"
# En Dash and Em Dash
puncs += "\u2013\u2014"


def main(argv):
    """ Takes in flextext and returns lines like "theword\tthe-word". """
    for line in fileinput.input(argv[1:]):
        line = line.replace('_', ' ')
        line = re.sub(r"\s*-+\s*", "-", line)
        # TODO: Decide how to deal with "~" shared syllables.
        # Remove punctuation
        line = re.sub(r"[" + puncs + r"]+\s+", ' ', line)
        line = re.sub(r"\s+[" + puncs + r"]+", ' ', line)
        line = re.sub(r"[" + puncs + r"]+$", '', line)
        line = re.sub(r"^[" + puncs + r"]+", '', line)
        line = re.sub(r"\s+", ' ', line)
        # TODO: Deal with double quotes.
        # line = line.replace('"', '')

        words = [x for x in line.split(' ') if x != '']
        for word in words:
            print(word.replace('-', '').lower() + "\t" + word.lower())


if __name__ == "__main__":  # pragma: no cover
    sys.exit(main(sys.argv))
