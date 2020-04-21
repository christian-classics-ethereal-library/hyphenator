#!/usr/bin/env python3
import fileinput
import re
import sys


def main(argv):
    for line in fileinput.input(argv[1:]):
        print(flexToText(line))


def flexToText(text):
    text = removeLilyCommands(text)
    text = re.sub(r" +", " ", text)
    text = text.replace(' -- ', '')
    text = text.replace('~', ' ')
    # Mid-word underscores behave like tildes.
    text = text.replace('_', ' ')
    return text.strip()


def removeLilyCommands(text):
    # Remove some lilypond commands
    # (Especially those that often appear inline with text)
    text = re.sub(r" *\\bold *", " ", text)
    text = re.sub(r" *\\italic *", " ", text)
    text = re.sub(r" *\\line *", " ", text)
    text = re.sub(r" *\\markup *", " ", text)
    text = re.sub(r" *%remove when \w+!?=\w+ *", " ", text)
    text = re.sub(r" *%endremove *", " ", text)
    text = re.sub(r" *\\set\s+\S+\s*=\s*\S+ *", " ", text)
    text = re.sub(r" *\\skip *[0-9]+ *", " ", text)
    text = re.sub(r" *\\slurOff *", " ", text)
    text = re.sub(r" *\\slurOn *", " ", text)
    # This is problematic, as smallCaps { Lord } != LORD
    text = re.sub(r" *\\smallCaps *", " ", text)
    text = re.sub(r" *\\switch\S+ *", " ", text)
    text = re.sub(r" *\\tiny *", " ", text)
    text = re.sub(r" *\\unset\s+\S+ *", " ", text)
    text = re.sub(r" *} *", " ", text)
    text = re.sub(r" *{ *", " ", text)
    text = re.sub("( _+)+ ", ' ', text)
    text = re.sub("^_+ ", '', text)
    text = re.sub(" _+$", '', text)
    text = re.sub(r'"(\*\w*)"', r'\1', text)
    return text


if __name__ == "__main__":  # pragma: no cover
    sys.exit(main(sys.argv))
