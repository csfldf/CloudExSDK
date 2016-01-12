#!/usr/bin/env python
# encoding: utf-8

import re

def isNumber(strToTest):
    pattern = r'^\d+$'
    m = re.match(pattern, strToTest)
    if m:
        return True
    else:
        return False

def errorResultJson(msg):
    return {'error' : msg}

def successResultJson(msg):
    return {'success' : msg}


def avgNumberList(nl):
    avg = float(sum(nl)) / len(nl)
    return round(avg, 2)

def popNoneInList(targetList):
    for item in targetList:
        if not item:
            targetList.remove(item)

