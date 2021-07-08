import datetime as dt
from typing import List, TypedDict

from src.typeDefs.violRow import IViolRow


class IReportCxt(TypedDict):
    reportFilePath: str
    reportHeading: str
    reportDtObj: dt.datetime
    reportDt: str
    atcViolRows: List[IViolRow]
    ttcViolRows: List[IViolRow]
