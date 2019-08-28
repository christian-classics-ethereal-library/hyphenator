# Hyphenator

A tool to analyze and create flexText verses.

## Setup

`pip3 install -r requirements.txt`
`python3 -c "import nltk; nltk.download('cmudict')"`

## Usage

### getVerses

`./getVerses.sh path/to/*.yaml`

### meterify

`./getVerses.sh path/to/file.yaml | python3 -m hyphenator.meterify | sort -u`

### wordSyl

`./getVerses.sh path/to/*.yaml | python3 -m hyphenator.wordSyl | sort | uniq -c`

### makeDict

`cat sortedWordSylOutput.txt | python3 -m hyphenator.makeDict > dict.yaml`

### textToFlex

```python
import hyphenator.textToFlex
mst = hyphenator.textToFlex.MultiSylT('-')
mst.multiTokenize("offering")
hyphenator.textToFlex.syllabizeLine("Amazing grace, how sweet the sound!", 8, mst)
```

## [Core Understanding Test (CUT)](https://gitlab.ccel.org/drupal/shared-modules/wikis/Core-Understanding-Test)

- What is the meter of a hymn and how is it represented?
- What sources does Hyphenator use to split a word into syllables?
- How does Hyphenator treat punctuation and apostrophes when creating flextext?
- How could a file like `hyphenator/dict.yaml` be created?
- How does meterify determine the meter of a stanza?
