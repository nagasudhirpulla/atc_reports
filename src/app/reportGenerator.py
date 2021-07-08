import datetime as dt
import os

from docxtpl import DocxTemplate
from src.app.getDateRangeForInpDt import getDateRangeForInpDt
from src.config.appConfig import getAppConfig
from src.logging.appLogger import getAppLogger
from src.typeDefs.reportContext import IReportCxt
from src.services.dataFetcher import fetchPntHistData


class ReportGenerator:

    def __init__(self):
        self.appLogger = getAppLogger()
        self.appConf = getAppConfig()

    def getReportContextObj(self, dateInp: dt.datetime) -> IReportCxt:
        """get the report context object for populating the report template
        Returns:
            IReportCxt: report context object
        """
        # get the report type
        reportType = self.appConf["reportType"]
        reportPrefix = self.appConf["reportPrefix"]

        # derive start and end dates for the report data
        (startDt, endDt) = getDateRangeForInpDt(dateInp, reportType)
        startDateReportString = dt.datetime.strftime(startDt, '%d-%b-%Y')
        endDateReportString = dt.datetime.strftime(endDt, '%d-%b-%Y')

        # derive report date as end date plus 1 day
        reportDt = endDt + dt.timedelta(days=1)
        reportDtStr = dt.datetime.strftime(reportDt, "%d-%b-%Y")

        # derive report heading and report filename
        reportHeading = ""
        reportFilename = ""
        if reportType == "d":
            reportHeading = "System Reliability Indices Report for {0}".format(
                startDateReportString)
            reportFilename = "{0}_{1}.docx".format(
                reportPrefix, dt.datetime.strftime(startDt, '%Y_%m_%d'))
        elif reportType == "w":
            reportHeading = "System Reliability Indices Report for the week from {0} to {1}".format(
                startDateReportString, endDateReportString)
            reportFilename = "{0}_{1}_{2}.docx".format(
                reportPrefix, dt.datetime.strftime(startDt, '%Y_%m_%d'), dt.datetime.strftime(endDt, '%Y_%m_%d'))
        elif reportType == "m":
            startDateMonthStr = dt.datetime.strftime(startDt, '%B %Y')
            reportHeading = "System Reliability Indices Report for the month of {0}".format(
                startDateMonthStr)
            reportFilename = "{0}_{1}.docx".format(
                reportPrefix, dt.datetime.strftime(startDt, '%Y_%m'))

        outputFolder = self.appConf["outputFolder"]
        reportFilePath = os.path.join(outputFolder, reportFilename)

        # TODO generate atc violation rows
        atcViolRows = []

        # TODO generate ttc violation rows
        ttcViolRows = []
        entities = self.appConf["entities"]
        apiBaseUrl: str = self.appConf["apiUrlBase"]
        isRandom: bool = self.appConf["isRandom"]
        for ent in entities:
            entName = ent[0]
            drawalPnt = ent[1]
            atcPnt = ent[2]
            ttcPnt = ent[3]
            drawalRows = fetchPntHistData(
                drawalPnt, apiBaseUrl, startDt, endDt, 'average', 900, self.appLogger, isRandom)

        # create context for weekly reoport
        reportContext: IReportCxt = {
            "reportFilePath": reportFilePath,
            "reportHeading": reportHeading,
            "reportDtObj": reportDt,
            "reportDt": reportDtStr,
            "atcViolRows": atcViolRows,
            "ttcViolRows": ttcViolRows
        }
        return reportContext

    def generateReportWithContext(self, reportContext: IReportCxt) -> bool:
        """generate the report file at the desired dump folder location
        based on the template file and report context object
        Args:
            reportContext (IReportCxt): report context object
        Returns:
            bool: True if process is success, else False
        """
        try:
            tmplPath = self.appConf["templatePath"]

            # derive the report path
            reportFilePath = reportContext["reportFilePath"]

            # render data into report
            doc = DocxTemplate(tmplPath)
            doc.render(reportContext)

            # save the report as a word file
            doc.save(reportFilePath)
        except Exception as err:
            self.appLogger.error(
                "error while saving report from context", exc_info=err)
            return False
        return True

    def generateReport(self, dateInp: dt.datetime) -> bool:
        """generates and dumps weekly report for given dates at a desired location based on a template file
        Args:
            dateInp (dt.datetime): input date
        Returns:
            bool: True if process is success, else False
        """
        reportCtxt = self.getReportContextObj(dateInp)
        isSuccess = self.generateReportWithContext(
            reportCtxt)
        # convert report to pdf
        # convert(dumpFileFullPath, dumpFileFullPath.replace('.docx', '.pdf'))
        return isSuccess
