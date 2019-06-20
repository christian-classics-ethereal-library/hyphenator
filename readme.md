# Hyphenator

A tool to analyze and create flexText verses.

## Setup

`pip3 install -r requirements.txt`

## Usage

### getVerses

`./getVerses.sh path/to/*.yaml`

### meterify

`./getVerses.sh path/to/file.yaml | ./meterify.py | sort -u`

### wordSyl

`./getVerses.sh path/to/*.yaml | ./wordSyl.py | sort | uniq -c`

### makeDict

`cat sortedWordSylOutput.txt | ./makeDict.py > dict.yaml`
