#!/usr/bin/env python3
import tempfile
import yaml

from hyphenator import textToFlex
from hyphenator import flexToText


def test_stderr_output_is_YAML(capsys):
    textToFlex.main(['', '8.16.8.6', '-', 'tests/dict.yaml', '',
                     'tests/amazinggraceV2.raw.txt'])
    captured = capsys.readouterr()
    messages = yaml.safe_load(captured.err)
    assert {
        'error':
        "Unable to syllabize 'And grace my fears relieved;' to 16 syllables"
    } in messages


def test_textToFlex_main(capsys):
    textToFlex.main(['', '8.6.8.6', '-', 'tests/dict.yaml', '',
                     'tests/amazinggraceV2.raw.txt'])
    captured = capsys.readouterr()
    messages = yaml.safe_load(captured.err)
    assert messages is None
    assert "The hour I first be -- lieved!" in captured.out


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
    assert ["ALL?"] == mst.reformat(["all"], "ALL?")


def test_spanishTokenize():
    mst = textToFlex.MultiSylT('tests/dict.yaml', lang='es')
    # Two strong vowels (see TODO for double-l)
    assert len(["to", "a", "lla"]) == len(mst._spanishTokenize("toalla"))
    # Weak + Strong vowel
    assert ["i", "gua", "na"] == mst._spanishTokenize("iguana")
    # Two weak vowels
    assert ["rei", "na"] == mst._spanishTokenize("reina")
    # Accented vowel
    assert ["tí", "o"] == mst._spanishTokenize("tío")
    # Ending consonant
    assert ["com", "pre", "sar"] == mst._spanishTokenize("compresar")


def test_spanish_syllabize():
    mst = textToFlex.MultiSylT('tests/dict.yaml', lang='es')
    line = "Santificado sea tu nombre"
    result = textToFlex.syllabizeLine(line, 10, mst)
    assert 'es' == mst.lang
    assert "San -- ti -- fi -- ca -- do se -- a tu nom -- bre" in result
