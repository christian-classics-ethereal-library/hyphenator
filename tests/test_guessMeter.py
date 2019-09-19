#!/usr/bin/env python3
from hyphenator import guessMeter


def test_guessMeter(capsys):
    guessMeter.main(['', 'en', 'tests/amazinggraceV2.raw.txt'])
    captured = capsys.readouterr()
    assert captured.out.strip() == "8.6.8.6"


def test_guessMeter_function():
    output = guessMeter.guessMeter('Amazing\r\nGrace How', 'en')
    assert "3.2" == output
