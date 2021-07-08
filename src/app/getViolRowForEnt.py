import datetime as dt
from typing import Tuple

from src.logging.appLogger import getAppLogger
from src.services.dataFetcher import fetchPntHistData
from src.typeDefs.violRow import IViolRow


def getViolRowForEnt(apiBaseUrl: str, startDt: dt.datetime, endDt: dt.datetime, entName: str, drawalPnt: str, atcPnt: str, ttcPnt: str, isRandom: bool) -> Tuple[IViolRow, IViolRow]:
    appLogger = getAppLogger()

    # fetch data samples
    drawalRows = fetchPntHistData(
        drawalPnt, apiBaseUrl, startDt, endDt, 'average', 900, appLogger, isRandom)
    atcRows = fetchPntHistData(
        atcPnt, apiBaseUrl, startDt, endDt, 'average', 900, appLogger, isRandom)
    ttcRows = fetchPntHistData(
        ttcPnt, apiBaseUrl, startDt, endDt, 'average', 900, appLogger, isRandom)

    # create violation summary rows
    atcViolRow: IViolRow = None
    ttcViolRow: IViolRow = None

    if len(drawalRows) == len(atcRows):
        numAtcViolBlks = len([True for sIter in range(
            len(drawalRows)) if drawalRows[sIter]["dval"] > atcRows[sIter]["dval"]])
        atcViolRow = {
            "srNum": 1,
            "stateName": entName,
            "numBlks": numAtcViolBlks,
            "numHrs": round(numAtcViolBlks/4, 1),
            "percHrs": round(100*numAtcViolBlks/len(drawalRows), 1)
        }

    if len(drawalRows) == len(ttcRows):
        numTtcViolBlks = len([True for sIter in range(
            len(drawalRows)) if drawalRows[sIter]["dval"] > ttcRows[sIter]["dval"]])
        ttcViolRow = {
            "srNum": 1,
            "stateName": entName,
            "numBlks": numTtcViolBlks,
            "numHrs": round(numTtcViolBlks/4, 1),
            "percHrs": round(100*numTtcViolBlks/len(drawalRows), 1)
        }

    return (atcViolRow, ttcViolRow)
