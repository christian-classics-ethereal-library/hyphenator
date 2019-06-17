#!/bin/bash
./getVerses.py $@ | grep -v "{" | grep -v "}" | grep "=" -v | grep "\\\\" -v | grep '%' -v
