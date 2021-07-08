from typing import TypedDict


class IViolRow(TypedDict):
    srNum: int
    stateName: str
    numBlks: int
    numHrs: float
    percHrs: float
