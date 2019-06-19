# Hyphenator

A tool to analyze and create flexText verses.

## Setup

`pip3 install -r requirements.txt`

## Usage

### getVerses

`./getVerses.sh path/to/*.yaml`

### meterify

`./getVerses.sh path/to/file.yaml | python3 -m hyphenator.meterify | sort -u`

### wordSyl

`./getVerses.sh path/to/*.yaml | python3 -m hyphenator.wordSyl | sort | uniq -c`

### makeDict

`cat sortedWordSylOutput.txt | python3 -m hyphenator.makeDict > dict.yaml`
