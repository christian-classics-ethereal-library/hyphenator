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


def test_multiTokenize_plural():
    mst = textToFlex.MultiSylT('tests/dict.yaml')
    off = list(mst.multiTokenize('offerings'))
    assert ['off', 'erings'] in off
    assert ['of', 'fer', 'ings'] in off


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
    assert "calv'ry's" == mst.deformat("Calv\u2019ry\u2019s")
    assert "'tis" == mst.deformat("\u2018tis")


def test_reformat_function():
    mst = textToFlex.MultiSylT('tests/dict.yaml')
    assert ["All?"] == mst.reformat(["all"], "All?")
    assert ["ALL?"] == mst.reformat(["all"], "ALL?")
    assert ["Cal", "v\u2019ry\u2019s"] == mst.reformat(
        ["cal", "v'ry's"], "Calv\u2019ry\u2019s")
    assert ["Cal", "v'ry\u2019s"] == mst.reformat(
        ["cal", "v'ry's"], "Calv'ry\u2019s")
    ordered = "\u2018'\u2019"
    assert [ordered] == mst.reformat(["'''"], ordered)


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


def test_smash_words_together():
    mst = textToFlex.MultiSylT('tests/dict.yaml', lang='es')
    line = "Tú el alfarero, yo el barro soy."
    result = textToFlex.syllabizeLine(line, 9, mst, lang='es')
    assert "Tú~el al -- fa -- re -- ro, yo~el ba -- rro soy." in result
    result = textToFlex.syllabizeLine(line, 8, mst, lang='es')
    assert [] == result


def test_smash_words_ignore_character():
    mst = textToFlex.MultiSylT('tests/dict.yaml', lang='es')
    line = "te adorará todo hombre"
    result = textToFlex.syllabizeLine(line, 7, mst, lang='es')
    assert "te~a -- do -- ra -- rá to -- do~hom -- bre" in result


def test_cjk_syllabize():
    mst = textToFlex.MultiSylT('tests/dict.yaml', lang='zh')
    c = '聖哉，聖哉，聖哉，慈悲全能主宰，'
    result = textToFlex.syllabizeLine(c, 12, mst, lang='zh')
    assert '聖 -- 哉， 聖 -- 哉， 聖 -- 哉， 慈 -- 悲 -- 全 -- 能 -- 主 -- 宰，' \
        in result
    j = "よろずのくにびと、 "
    result = textToFlex.syllabizeLine(j, 8, mst, lang='ja')
    assert "よ -- ろ -- ず -- の -- く -- に -- び -- と、" in result
    k = "너희는 먼저- 추의 나라위"
    result = textToFlex.syllabizeLine(k, 10, mst, lang='ko')
    assert "너 -- 희 -- 는 먼 -- 저- 추 -- 의 나 -- 라 -- 위" in result
