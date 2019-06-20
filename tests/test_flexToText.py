#!/usr/bin/env python3
import tempfile
import yaml

from hyphenator import flexToText


def test_flexToText(capsys):
    flexToText.main(['', 'tests/amazinggraceV1.flex.txt'])
    captured = capsys.readouterr()
    assert captured.out[:34] == "Amazing grace! How sweet the sound"
