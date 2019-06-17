#!/bin/bash
./getVerses.py $1 | grep -v "{" | grep -v "}" | grep "=" -v | grep "\\\\" -v | grep '%' -v
