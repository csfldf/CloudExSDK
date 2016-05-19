#!/usr/bin/python
__author__ = 'Darkness_Y'

import os
import sys

if __name__ == '__main__':
    init = bool(int(sys.argv[1]))
    result = 0.0
    fn = "cpuInfo.data"
    line = os.popen("cat /proc/stat").readline()
    if not init:
        util_cur = line.split(" ")
        util_pre = open(fn).readline().split(" ")
        total_pre = total_cur = 0;
        length = len(util_cur)
        for i in range(2, length):
            total_cur += int(util_cur[i])
            total_pre += int(util_pre[i])
        total = total_cur - total_pre
        idle = int(util_cur[5]) - int(util_pre[5])
        result = (1.0 * total - idle) / total
        print result
    mFile = open(fn, "w")
    mFile.write(line)
    mFile.close()

