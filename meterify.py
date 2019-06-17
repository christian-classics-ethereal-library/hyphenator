#!/usr/bin/env python3
import fileinput
import re
import sys


def main(argv):
    for line in fileinput.input():
        line = line.replace('_', ' ')
        line = line.replace('-', ' ')
        line = re.sub(r" +", " ", line)
        line = line.replace('\r', '')
        line = line.replace('\n', '')
        spaces = line.count(' ')
        number = len([x for x in line.split(' ') if x != ''])
        if(spaces and number):
            sys.stdout.write(str(number) + ".")
        else:
            print(line)


if __name__ == "__main__":
    sys.exit(main(sys.argv))
