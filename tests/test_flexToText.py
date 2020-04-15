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
    output = flexToText.flexToText(
        "Praise _ _ to thine _ e -- ter -- _ nal  mer -- it,")
    assert "Praise to thine eternal merit," == output
    output = flexToText.flexToText("this __ may be __ our end -- less  song:")
    assert "this may be our endless song:" == output


def test_tildeUnderscoreRemoved():
    output = flexToText.flexToText("no -- che de~a -- mor")
    assert "noche de amor" == output
    output = flexToText.flexToText("but I am_the Dance, and_I still go on.")
    assert "but I am the Dance, and I still go on." == output


def test_removeLilyCommands():
    output = flexToText.removeLilyCommands(
        "shall \\set ignoreMelismata = #t praise")
    assert "shall praise" == output
    output = flexToText.removeLilyCommands(
        "art \\unset ignoreMelismata ho -- ly;")
    assert "art ho -- ly;" == output
    output = flexToText.removeLilyCommands(
        "ye have seen his \\skip 1 na -- tal star:")
    assert "ye have seen his na -- tal star:" == output
    output = flexToText.removeLilyCommands(
        'vi -- sions of "*rap" -- ture now burst on my sight;')
    assert "vi -- sions of *rap -- ture now burst on my sight;" == output
    output = flexToText.removeLilyCommands(
        "a --\n%remove when separateStanzas=true\n _ \n%endremove\nmen")
    assert "a --\n \n \n \nmen" == output
