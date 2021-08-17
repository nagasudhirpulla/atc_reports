import datetime as dt
from typing import Tuple

from src.app.timeUtils import addMonths, getMondayBeforeDt, getSundayAfterDt


def getDateRangeForInpDt(inpDt: dt.datetime, repType: str) -> Tuple[dt.datetime, dt.datetime]:
    startDt = None
    endDt = None
    if repType in ["d", "ds"]:
        startDt = dt.datetime(inpDt.year, inpDt.month, inpDt.day)
        endDt = dt.datetime(inpDt.year, inpDt.month, inpDt.day, 23, 59)
    elif repType == "w":
        startDt = getMondayBeforeDt(inpDt)
        endDt = getSundayAfterDt(startDt)
        endDt = dt.datetime(endDt.year, endDt.month, endDt.day, 23, 59)
    elif repType == "m":
        startDt = dt.datetime(inpDt.year, inpDt.month, inpDt.day)
        endDt = addMonths(startDt, 1) - dt.timedelta(days=1)
        endDt = dt.datetime(endDt.year, endDt.month, endDt.day, 23, 59)
    return (startDt, endDt)
