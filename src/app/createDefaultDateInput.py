import datetime as dt

from src.app.timeUtils import addMonths


def createDefaultDateInput(repType: str) -> dt.datetime:
    nowDt = dt.datetime.now()
    resDt = None
    if repType == "d":
        resDt = dt.datetime(nowDt.year, nowDt.month,
                            nowDt.day) - dt.timedelta(days=1)
    elif repType == 'w':
        resDt = nowDt-dt.timedelta(days=7)
        resDt = dt.datetime(resDt.year, resDt.month, resDt.day)
    elif repType in ['m', 'ds']:
        resDt = dt.datetime(nowDt.year, nowDt.month, 1)
        resDt = addMonths(resDt, -1)
    return resDt
