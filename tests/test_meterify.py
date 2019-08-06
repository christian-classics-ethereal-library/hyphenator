#!/usr/bin/env python3
from hyphenator import meterify


def test_meterify(capsys):
    meterify.main(['', 'tests/amazinggraceV1.flex.txt'])
    captured = capsys.readouterr()
    assert captured.out == "8.6.8.6."


def test_meterify_function():
    output = meterify.meterify('A -- ma -- zing\r\nGrace How')
    assert "3.2" == output[0].strip('.')
