#!/usr/bin/env python
# encoding: utf-8

import re

periodRecoderFile = '/home/sk/image/cloudExData/periodRecoder.db'
periodRecoder = 'PERIODRECODER'

provisionInfoFile = '/home/sk/image/cloudExData/provisionInfo.db'
predictProvisionVMNumbers = 'PPVMN'
reactiveProvisionVMNumbers = 'RPVMN'

def isNumber(strToTest):
    pattern = r'^\d+$'
    m = re.match(pattern, strToTest)
    if m:
        return True
    else:
        return False


def isDecimal(strToTest):
    if not strToTest:
        return False

    pattern = r'^\d+\.\d+$'
    m = re.match(pattern, strToTest)
    if m:
        return True
    else:
        return False


def errorResultJson(msg):
    return {'error': msg}


def successResultJson(msg):
    return {'success': msg}


def avgNumberList(nl):
    avg = float(sum(nl)) / len(nl)
    return round(avg, 2)


def popNoneInList(targetList):
    for item in targetList:
        if not item:
            targetList.remove(item)
