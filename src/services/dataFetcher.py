import datetime as dt
import json
import random

import requests


def makeTwoDigits(num):
    if(num < 10):
        return "0"+str(num)
    return num


def fetchPntHistData(pnt, baseUrl: str, startTime: dt.datetime, endTime: dt.datetime, fetchStrategy: str = 'snap', secs: int = 60, logger=None, isRandom: bool = False):
    if isRandom:
        return fetchPntHistDataRandom(startTime, endTime, secs)

    startTimeStr = startTime.strftime('%d/%m/%Y/%H:%M:%S')
    endTimeStr = endTime.strftime('%d/%m/%Y/%H:%M:%S')

    params = dict(
        pnt=pnt,
        strtime=startTimeStr,
        endtime=endTimeStr,
        secs=secs,
        type=fetchStrategy
    )
    data = []
    try:
        # http://localhost:1234/api/values/history?pnt=WP.SCADA.F12453472&strtime=12/12/2019/00:00:00&endtime=13/12/2019/00:00:00&secs=900&type=average
        r = requests.get(
            url=baseUrl, params=params)
        data = json.loads(r.text)
        r.close()
    except Exception as e:
        data = []
        logger.error(e)
    return data


def fetchPntHistDataRandom(startTime: dt.datetime, endTime: dt.datetime, secs: int = 300):
    data = []
    if startTime > endTime:
        return data
    samplPeriod = secs
    samplPeriod = 60 if samplPeriod == 0 else samplPeriod

    curTime = startTime
    while curTime <= endTime:
        data.append({"dval": random.randint(-50, 50),
                     "timestamp": dt.datetime.strftime(curTime, "%Y-%m-%dT%H:%M:%S"),
                     "status": "GOOD"})
        curTime += dt.timedelta(seconds=samplPeriod)
    return data
