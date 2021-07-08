import calendar
import datetime as dt


def addMonths(inpDt: dt.datetime, mnths: int):
    tmpMnth = inpDt.month - 1 + mnths

    # Add floor((input month - 1 + k)/12) to input year component to get result year component
    resYr = inpDt.year + tmpMnth // 12

    # Result month component would be (input month - 1 + k)%12 + 1
    resMnth = tmpMnth % 12 + 1

    # Result day component would be minimum of input date component and max date of the result month (For example we cant have day component as 30 in February month)
    # Maximum date in a month can be found using the calendar module monthrange function as shown below
    resDay = min(inpDt.day, calendar.monthrange(resYr, resMnth)[1])

    # construct result datetime with the components derived above
    resDt = dt.datetime(resYr, resMnth, resDay, inpDt.hour,
                        inpDt.minute, inpDt.second, inpDt.microsecond)

    return resDt


def getMondayBeforeDt(inpDt: dt.datetime) -> dt.datetime:
    """ gets the first Monday before a specified date
    Args:
        inpDt (dt.datetime): input date
    Returns:
        dt.datetime: first monday before input date
    """
    # get first Monday before inpDt
    inpMonday = inpDt
    while not dt.datetime.strftime(inpMonday, '%w') == '1':
        inpMonday = inpMonday - dt.timedelta(days=1)
    return inpMonday


def getSundayAfterDt(inpDt: dt.datetime) -> dt.datetime:
    """ gets the first Sunday after a specified date
    Args:
        inpDt (dt.datetime): input date
    Returns:
        dt.datetime: first Sunday after input date
    """
    inpSunday = inpDt
    while not dt.datetime.strftime(inpSunday, '%w') == '0':
        inpSunday = inpSunday + dt.timedelta(days=1)
    return inpSunday
