from typing import TypedDict


class IViolRow(TypedDict):
    srNum: int
    stateName: str
    numBlks: int
    num_hrs: float
    perc_hrs: float
