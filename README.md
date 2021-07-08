## Report types
* Daily
* Weekly
* Monthly

## config file
* apiUrlBase - base url of data api
* isRandom - use random data for testing purposes
* entities - array of entities. Each entity is defined by the array ```["Name", "drawal pnt", "atc pnt", "ttc pnt"]```
* reportType - one of d(daily), w(weekly), m(monthly)
* dateInput - input date for report in the format "%Y-%m-%d" (example: 2021-12-31), for default value keep it as null
* outputFolder - Path of ouput folder where reports are dumped
* templatePath - Path of report template file
* reportPrefix - Prefix of the generated report file name

### Deriving default date input
* Check for report type
* If report type is daily, make default date input as yesterday
* If report type is weekly, make default date input as d-7
* If report type is monthly, make default date input as the first day of previous month

### Deriving report date range from date input
* For daily report the date range will be 0 to 24 hrs of date input
* For weekly report the date range will be 0 hrs of the week start date (Monday) to 24 hrs of week end date (Sunday) of date input
* For monthly report the date range will be 0 hrs of the month start date to 24 hrs of month end date of date input