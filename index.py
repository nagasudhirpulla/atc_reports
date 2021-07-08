import argparse
import datetime as dt

from src.app.createDefaultDateInput import createDefaultDateInput
from src.app.reportGenerator import ReportGenerator
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
        "Unable to get default input date, please check if reportType is either d, w, m...")
    exit()

# derive input date
dateInpStr: str = appConf['dateInput']
dateInp = defaultInpDate
if not dateInpStr == None:
    dateInp = dt.datetime.strptime(dateInpStr, "%Y-%m-%d")


# generate report
rprtGntr = ReportGenerator()
isReportGenSuccess: bool = rprtGntr.generateReport(dateInp)
if isReportGenSuccess:
    logger.info('System Reliability report file generation done!')
else:
    logger.error('System Reliability report file generation unsuccessful...')
