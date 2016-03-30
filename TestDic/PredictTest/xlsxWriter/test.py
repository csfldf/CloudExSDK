#!/usr/bin/env python
# encoding: utf-8
import re

f = open('./testTxt.txt')
for line in f:
    sl = re.split('[ \n]', line)
    print sl
f.close()
