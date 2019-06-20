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
