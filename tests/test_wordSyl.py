#!/usr/bin/env python3
from hyphenator import wordSyl


def test_meterify(capsys):
    wordSyl.main(['tests/amazinggraceV1.flex.txt'])
    captured = capsys.readouterr()
    assert captured.out[0:29] == "amazing\ta-maz-ing\ngrace\tgrace"
