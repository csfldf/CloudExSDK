#!/usr/bin/env python
# encoding: utf-8

import shelve
import re
from PredictUtil import *
from NormalUtil import popNoneInList
from PredictUtil.PeriodicPredictUtil import PeriodicPredictUtil
from PredictUtil.MAPredictUtil import MAPredictUtil
from PredictUtil.DailyPredictUtil import DailyPredictUtil
from PredictUtil.ACRCPredictUtil import ACRCPredictUtil

f = open('../DataFile/workload.txt')
for item in f:
    print item
