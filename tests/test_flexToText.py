#!/usr/bin/env python3
import tempfile
import yaml

from hyphenator import flexToText


def test_flexToText(capsys):
    flexToText.main(['', 'tests/amazinggraceV1.flex.txt'])
    captured = capsys.readouterr()
    assert captured.out[:34] == "Amazing grace! How sweet the sound"


def test_textStripped():
    output = flexToText.flexToText(" \tA -- ma -- zing\r\n")
    assert "Amazing" == output


def test_tildeRemoved():
    output = flexToText.flexToText("no -- che de~a -- mor")
    assert "noche de amor" == output


def test_removeLilyCommands():
    output = flexToText.removeLilyCommands(
        "shall \\set ignoreMelismata = #t praise")
    assert "shall praise" == output
    output = flexToText.removeLilyCommands(
        "art \\unset ignoreMelismata ho -- ly;")
    assert "art ho -- ly;" == output
