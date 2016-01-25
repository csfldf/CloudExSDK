#!/usr/bin/env python
# encoding: utf-8

topoFilePath = '/home/sk/openstackPythonSDKTest/ConfigDic/CloudTopo'
slaConfFilePath = '/home/sk/openstackPythonSDKTest/ConfigDic/SLA.config'

def analyseJsonFormatConfigFile(configFileName):
    if not configFileName:
        raise Exception('no configFileName!')

    cf = open(configFileName)
    cfContentList = cf.readlines()
    cfContent = ''

    for line in cfContentList:
        cfContent += line.strip()

    return eval(cfContent)





