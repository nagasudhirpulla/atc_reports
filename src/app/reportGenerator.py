import datetime as dt
import os

import pandas as pd
from docxtpl import DocxTemplate
from src.app.getDateRangeForInpDt import getDateRangeForInpDt
from src.app.getViolRowForEnt import getViolRowForEnt
from src.config.appConfig import getAppConfig
from src.logging.appLogger import getAppLogger
from src.typeDefs.reportContext import IReportCxt
from docx2pdf import convert

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
            reportHeading = "दैनिक प्रणाली विश्वसनीयता सूचकांक की आख्या दिनाँक /Daily System Reliability Indices Report for {0}".format(
                startDateReportString)
            reportFilename = "{0}_{1}.docx".format(
                reportPrefix, dt.datetime.strftime(startDt, '%Y_%m_%d'))
        elif reportType == "ds":
            reportHeading = ""
            reportFilename = ""
        elif reportType == "w":
            reportHeading = "साप्ताहिक प्रणाली विश्वसनीयता सूचकांक की आख्या/ Weekly System Reliability Indices Report for the week {0} to {1}".format(
                startDateReportString, endDateReportString)
            reportFilename = "{0}_{1}_{2}.docx".format(
                reportPrefix, dt.datetime.strftime(startDt, '%Y_%m_%d'), dt.datetime.strftime(endDt, '%Y_%m_%d'))
        elif reportType == "m":
            startDateMonthStr = dt.datetime.strftime(startDt, '%B %Y')
            reportHeading = "मासिक प्रणाली विश्वसनीयता सूचकांक की आख्या/ Monthly System Reliability Indices Report for {0}".format(
                startDateMonthStr)
            reportFilename = "{0}_{1}.docx".format(
                reportPrefix, dt.datetime.strftime(startDt, '%Y_%m'))

        outputFolder = self.appConf["outputFolder"]
        reportFilePath = os.path.join(outputFolder, reportFilename)

        # generate atc and ttc violation rows
        atcViolRows = []
        ttcViolRows = []

        entities = self.appConf["entities"]
        apiBaseUrl: str = self.appConf["apiUrlBase"]
        dataSource: str = self.appConf.get("dataSource", "scada")
        for rIter, ent in enumerate(entities):
            entName = ent[0]
            drawalPnt = ent[1]
            atcPnt = ent[2]
            ttcPnt = ent[3]
            (atcRow, ttcRow) = getViolRowForEnt(apiBaseUrl, startDt,
                                                endDt, entName, drawalPnt, atcPnt, ttcPnt, dataSource)
            if not atcRow == None:
                atcRow["srNum"] = rIter+1
                atcViolRows.append(atcRow)
            if not ttcRow == None:
                ttcRow["srNum"] = rIter+1
                ttcViolRows.append(ttcRow)

        # create context for weekly reoport
        reportContext: IReportCxt = {
            "reportFilePath": reportFilePath,
            "reportHeading": reportHeading,
            "startDt": startDt,
            "endDt": endDt,
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

            # convert report to pdf
            convert(reportFilePath, reportFilePath.replace('.docx', '.pdf'))
        except Exception as err:
            self.appLogger.error(
                "error while saving report from context", exc_info=err)
            return False
        return True

    def generateReport(self, dateInp: dt.datetime, endDt: dt.datetime) -> bool:
        """generates and dumps weekly report for given dates at a desired location based on a template file
        Args:
            dateInp (dt.datetime): input date
        Returns:
            bool: True if process is success, else False
        """
        runLoop: bool = True
        targetDt: dt.datetime = dateInp
        while runLoop:
            reportCtxt = self.getReportContextObj(targetDt)
            isSuccess = self.generateReportWithContext(
                reportCtxt)            

            # derive target date for next iteration
            targetDt = reportCtxt["endDt"] + dt.timedelta(days=1)
            targetDt = dt.datetime(targetDt.year, targetDt.month, targetDt.day)

            # decide whether to perform next iteration
            runLoop = True if (targetDt <= endDt) else False
        return isSuccess

    def generateDaywiseStatsExcel(self, startDt: dt.datetime, endDt: dt.datetime) -> bool:
        if startDt > endDt:
            return False
        reportAtcRows = []
        reportTtcRows = []
        for targetDt in pd.date_range(start=startDt, end=endDt, freq='D'):
            targetDt: dt.datetime = targetDt.to_pydatetime()
            reportCtxt = self.getReportContextObj(targetDt)
            for atcRow in reportCtxt["atcViolRows"]:
                reportAtcRows.append(
                    [targetDt.date(), atcRow["stateName"], atcRow["numBlks"], atcRow["numHrs"], atcRow["percHrs"]])
            for ttcRow in reportCtxt["ttcViolRows"]:
                reportTtcRows.append(
                    [targetDt.date(), ttcRow["stateName"], ttcRow["numBlks"], ttcRow["numHrs"], ttcRow["percHrs"]])
        # derive the report excel file path
        reportPrefix = self.appConf["reportPrefix"]
        startDtStr = dt.datetime.strftime(startDt, '%Y_%m_%d')
        endDtStr = dt.datetime.strftime(endDt, '%Y_%m_%d')
        reportFilename = "{0}_{1}_{2}.xlsx".format(
            reportPrefix, startDtStr, endDtStr)
        outputFolder = self.appConf["outputFolder"]
        reportFilePath = os.path.join(outputFolder, reportFilename)
        # export data to the report excel file path
        with pd.ExcelWriter(reportFilePath) as writer:
            dfCols = ["Date", "Name", "NumBlocks", "NumHrs", "PercentageHrs"]
            pd.DataFrame(data=reportAtcRows, columns=dfCols).to_excel(
                writer, index=False, sheet_name='atc')
            pd.DataFrame(data=reportTtcRows, columns=dfCols).to_excel(
                writer, index=False, sheet_name='ttc')
        return True
