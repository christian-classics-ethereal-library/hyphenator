#!/bin/bash
python3 -m hyphenator.getVerses $@ | grep -v "{" | grep -v "}" | grep "=" -v | grep "\\\\" -v | grep '%' -v
