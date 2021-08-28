import argparse
import datetime as dt
from typing import Optional

from src.app.createDefaultDateInput import createDefaultDateInput
from src.app.reportGenerator import ReportGenerator
from src.app.timeUtils import addMonths
from src.config.appConfig import loadAppConfig
from src.logging.appLogger import initAppLogger

logger = initAppLogger()

# read command line inputs if any
# python index.py --config config/config.json
parser = argparse.ArgumentParser()
parser.add_argument("--config", help="Config json file path",
                    default="config/config.json")
args = parser.parse_args()

# read application configuration json
configFilePath = args.config
appConf = loadAppConfig(configFilePath)
reportType: str = appConf["reportType"]

# derive default input date
defaultInpDate = createDefaultDateInput(reportType)
if defaultInpDate == None:
    logger.error(
        "Unable to get default input date, please check if reportType is either d, w, m, ds...")
    exit()

# derive input date
dateInpStr: str = appConf['dateInput']
dateInp = defaultInpDate
if not dateInpStr == None:
    dateInp = dt.datetime.strptime(dateInpStr, "%Y-%m-%d")

endDateStr = appConf.get("endDate", None)
endDt: Optional[dt.datetime] = None
if not endDateStr == None:
    endDt = dt.datetime.strptime(endDateStr, "%Y-%m-%d")

# create a report generator instance
rprtGntr = ReportGenerator()

isReportGenSuccess: bool = False

if reportType in ["d", "w", "m"]:
    # derive end date
    endDt = endDt or dateInp

    # generate report
    isReportGenSuccess = rprtGntr.generateReport(dateInp, endDt)
elif reportType == "ds":
    # derive default end date from start date
    defaultEndDate = addMonths(dt.datetime(
        dateInp.year, dateInp.month, 1), 1) - dt.timedelta(days=1)

    # derive end date
    endDt = endDt or defaultEndDate

    # generate report
    isReportGenSuccess = rprtGntr.generateDaywiseStatsExcel(
        startDt=dateInp, endDt=endDt)

if isReportGenSuccess:
    logger.info('System Reliability report file generation done!')
else:
    logger.error('System Reliability report file generation unsuccessful...')
