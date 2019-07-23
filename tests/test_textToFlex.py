#!/usr/bin/env python3
import tempfile
import yaml

from hyphenator import textToFlex
from hyphenator import flexToText


def test_stderr_output_is_YAML(capsys):
    textToFlex.main(['', '8.6.8.6', '-', 'tests/dict.yaml',
                     'tests/amazinggraceV2.raw.txt'])
    captured = capsys.readouterr()
    messages = yaml.safe_load(captured.err)
    # ['re', 'lieved'] isn't in tests/dict.yaml
    assert {
        'warning': "['re', 'lie', 'ved'] has 3 syllables, expected: 2 or 2"
    } in messages
    assert {
        'error':
            "Unable to syllabize 'And grace my fears relieved;' to 6 syllables"
    } in messages
    # TODO: Test for the alternates key


def test_multiTokenize():
    mst = textToFlex.MultiSylT('tests/dict.yaml')
    off = list(mst.multiTokenize('offering'))
    assert ['off', 'ering'] in off
    assert ['of', 'fer', 'ing'] in off


def test_alternates():
    mst = textToFlex.MultiSylT('tests/dict.yaml')
    line = "offering offering"
    assert "off -- ering off -- ering" in textToFlex.syllabizeLine(
        line, 4, mst)
    off5 = textToFlex.syllabizeLine(line, 5, mst)
    assert "of -- fer -- ing off -- ering" in off5
    assert "off -- ering of -- fer -- ing" in off5


def test_reformat_singular():
    mst = textToFlex.MultiSylT('tests/dict.yaml')
    line = "All? all."
    syllabized = textToFlex.syllabizeLine(line, 2, mst)
    assert [line] == syllabized

    line2 = "all, All!"
    syllabized2 = textToFlex.syllabizeLine(line2, 2, mst)
    assert [line2] == syllabized2


def test_deformat_function():
    mst = textToFlex.MultiSylT('tests/dict.yaml')
    assert "all" == mst.deformat('All?')


def test_reformat_function():
    mst = textToFlex.MultiSylT('tests/dict.yaml')
    assert ["All?"] == mst.reformat(["all"], "All?")
