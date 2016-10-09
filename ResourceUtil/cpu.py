#!/usr/bin/python
import os

if __name__ == '__main__':
    infos = []
    fp = os.popen("cat /proc/cpuinfo")
    freqStandard = 0.0
    freqReal = 0.0
    thread = 0
    for line in fp.readlines():
        if line.startswith("model name"):
            if line.__contains__("@"):
                freqStandard = float(line.split("@")[1].split("GHz")[0]) * 1000
        elif line.startswith("cpu MHz"):
            freqReal = float(line.split(": ")[1])
            if freqStandard == 0.0:
                freqStandard = freqReal
        elif line.startswith("siblings"):
            thread = int(line.split(": ")[1])
            infos.append([thread, freqStandard, freqReal])
    print infos

