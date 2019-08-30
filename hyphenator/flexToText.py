#!/usr/bin/env python3
import fileinput
import re
import sys


def main(argv):
    for line in fileinput.input(argv[1:]):
        print(flexToText(line))


def flexToText(text):
    text = text.replace(' _ ', ' ')
    text = re.sub(r" +", " ", text)
    text = removeLilyCommands(text)
    text = text.replace(' -- ', '')
    text = text.replace('~', ' ')
    return text.strip()


def removeLilyCommands(text):
    # Remove some lilypond commands that often appear inline with text
    text = re.sub(r" *\\set\s+\S+\s*=\s*\S+ *", " ", text)
    text = re.sub(r" *\\unset\s+\S+ *", " ", text)
    text = re.sub(r" *\\slurOff *", " ", text)
    text = re.sub(r" *\\slurOn *", " ", text)
    text = re.sub(r" *\\switch\S+ *", " ", text)
    text = re.sub(r" *\\(line|italic|bold) *{? *", " ", text)
    text = re.sub(r" *} *", " ", text)
    return text


if __name__ == "__main__":  # pragma: no cover
    sys.exit(main(sys.argv))
