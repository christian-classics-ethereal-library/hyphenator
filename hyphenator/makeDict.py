#!/usr/bin/env python3
import fileinput
import json
import re
import sys


def main(argv):
    """Takes a sorted list with entries like "32 theword the-word"
    and outputs a YAML dict.
    """
    prevWord = None
    print("words:")
    for line in fileinput.input(argv):
        line = re.sub(r"^ *", "", line)
        line = line.replace(" ", "\t")
        line = line.replace("\n", "")
        parts = line.split("\t")
        freq = parts[0]
        word = parts[1]
        hyphenated = parts[2].split('-')

        if(word != prevWord):
            print("  " + json.dumps(word) + ":")
        print("  - " + json.dumps(hyphenated))
        prevWord = word


if __name__ == "__main__": # pragma: no cover
    sys.exit(main(sys.argv))
