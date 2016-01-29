#!/usr/bin/env python
# encoding: utf-8

import logging


def getLogUtil(loggerName, logLevel=logging.INFO):
    logger = logging.getLogger(loggerName)
    logger.setLevel(logLevel)
    fh = logging.FileHandler('/home/sk/image/cloudExLog/' + loggerName + '.log')
    formatter = logging.Formatter('%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s')
    fh.setFormatter(formatter)
    logger.addHandler(fh)
    return logger
