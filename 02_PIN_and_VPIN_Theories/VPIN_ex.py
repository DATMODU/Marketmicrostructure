# -*- codings : utf-8 -*-

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import time
import os

def calDivide(a, b):
    quotient = a // b
    remainder = a % b
    return quotient, remainder

bucketCap = 370
futures = pd.read_csv('FuturesTrade.csv', index_col=0, parse_dates=True)

remainderB = remainderS = 0
buyV = sellV = 0
bucket = []
timedelta = []
bStacked = False
stTime = futures.index[0]
for idx, vol in enumerate(futures.volume):
    if bStacked:
        stTime = futures.index[idx]
        bStacked = False

    if vol >= 0:
        if vol >= bucketCap:
            if (buyV > 0 or sellV > 0) and buyV + sellV < bucketCap:
                temp = bucketCap - (buyV + sellV)
                bucket.append([buyV + temp ,sellV])
                vol -= temp
            quo, remainderB = calDivide(vol, bucketCap)
            for _ in range(quo):
                bucket.append([bucketCap, 0])
                timedelta.append(futures.index[idx] - futures.index[idx])
            bStacked = True
            buyV = remainderB
            remainderB = 0
            continue

        buyV += vol
        if buyV + sellV >= bucketCap:
            remainderB = buyV + sellV - bucketCap
            bucket.append([buyV - remainderB, sellV])
            bStacked = True
            buyV = remainderB
            sellV = 0
            remainderB = 0
            edTime = futures.index[idx]
            timedelta.append(edTime - stTime)
            stTime = edTime = 0

    else:
        if -vol >= bucketCap:
            if (buyV > 0 or sellV > 0) and buyV + sellV < bucketCap:
                temp = bucketCap - (buyV + sellV)
                bucket.append([buyV, sellV + temp])
                vol += temp
            quo, remainderS = calDivide(-vol, bucketCap)
            for _ in range(quo):
                bucket.append([0, bucketCap])
                timedelta.append(futures.index[idx] - futures.index[idx])
            bStacked = True
            sellV = remainderS
            remainderS = 0
            continue

        sellV += -vol
        if buyV + sellV >= bucketCap:
            remainderS = buyV + sellV - bucketCap
            bucket.append([buyV, sellV - remainderS])
            bStacked = True
            sellV = remainderS
            buyV = 0
            remainderS = 0
            edTime = futures.index[idx]
            timedelta.append(edTime - stTime)
            stTime = edTime = 0

bucket = pd.DataFrame(bucket, columns=['buy','sell'])
timeDelta = pd.Series(timedelta)
VPIN = np.abs(bucket.buy -  bucket.sell).sum() / (np.shape(bucket)[0] * bucketCap)