#!/usr/bin/env python3
from hyphenator import meterify


def test_meterify(capsys):
    meterify.main(['tests/amazinggraceV1.flex.txt'])
    captured = capsys.readouterr()
    assert captured.out == "8.6.8.6."
