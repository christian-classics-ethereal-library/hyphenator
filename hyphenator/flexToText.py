#!/usr/bin/env python3
import fileinput
import re


def main(argv):
    for line in fileinput.input(argv[1:]):
        print(flexToText(line))


def flexToText(text):
    text = text.replace(' _ ', ' ')
    text = re.sub(r" +", " ", text)
    text = text.replace(' -- ', '')
    return text.strip()


if __name__ == "__main__":  # pragma: no cover
    sys.exit(main(sys.argv))
