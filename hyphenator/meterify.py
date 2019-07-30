#!/usr/bin/env python3
import fileinput
import re
import sys


def main(argv):
    """ For a paragraph of flextext, will return the syllables in each line,
    separated by a period,
    like "8.6.8.6.".
    """
    for line in fileinput.input(argv[1:]):
        sys.stdout.write(process_line(line))


def meterify(paragraph):
    meter = ''
    for line in paragraph.split("\n"):
        meter += process_line(line)
    return meter


def process_line(line):
    line = line.replace('_', ' ')
    line = line.replace('-', ' ')
    line = re.sub(r" +", " ", line)
    line = line.replace('\r', '')
    line = line.replace('\n', '')
    spaces = line.count(' ')
    number = len([x for x in line.split(' ') if x != ''])
    if(spaces and number):
        return str(number) + "."
    else:
        return line + "\n"


if __name__ == "__main__":  # pragma: no cover
    sys.exit(main(sys.argv))
