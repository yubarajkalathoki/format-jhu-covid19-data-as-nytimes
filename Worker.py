import urllib.request
import csv

casesFile = open("us_cases.csv")
deathsFile = open("us_deaths.csv")

casesReader = csv.DictReader(casesFile)
deathsReader = csv.DictReader(deathsFile)

deathFileUrl = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_US.csv"
confirmedFileUrl = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_US.csv"
deathFileName = "deaths-us.csv"
confirmedFileName = "confirmed-us.csv"

# cr = {}

def downloadCSV(url, filename):
    print(f"Downloading {filename}")
    urllib.request.urlretrieve(url, filename)
    print(f"{filename} Download success!")


# deathData = []

headersColumn = ["date", "county", "state", "case", "death"]

class CSVData:
    date = ""
    county = ""
    state = ""
    case = 0
    death = 0

    def __init__(self, date, county, state, case = 0, death = 0):
        self.date = date
        self.county = county
        self.state = state
        self.case = case
        self.death = death

class DataDictionary(dict): 
  
    # __init__ function 
    def __init__(self): 
        self = dict() 
          
    # Function to add key:value 
    def add(self, key, value): 
        self[key] = value 


casesDictionary = DataDictionary()
deathsDictionary = DataDictionary()

def start():
    noOfColumns = len(next(casesReader))
    casesFile.seek(0) # starts to read from 0th index
    headerList = casesReader.fieldnames
    # print(headerList)
    dates = []
    for col in range(11, noOfColumns):
        dates.append(headerList[col])
    print(len(dates))
    confirmedList = []
    next(casesReader) # Skiping the headers row before processsing

    next(deathsReader) # Skiping the headers row before processsing
    
    listMaker = casesReader
    cr = list(listMaker)
    # for c in cr:
    #     print(c)
    dr = list(deathsReader)
    # print(f"len of cr {len(next(casesReader))}")
    dateList = list(dates)
    count = 0
    setTotalCases(list(dates), cr, dr)
    print("called total case method")
    for date in dateList:
        # print(date)
        tc = casesDictionary.get(date, "")
        # print(f"{date} -> {tc}")
        td = deathsDictionary.get(date, "")
        for row  in cr:
            count += 1
            #  print(f"Added {date}")
            confirmedList.append(CSVData(date, row["Admin2"], row["Province_State"], tc, td))
    print(count)
    writeCsv(confirmedList)


# def parseCSV(cases):
#     print(f"Processing {cases}")
#     casesFile = open(cases, newline="")
#     with casesFile:
#         readerData = csv.DictReader(casesFile)
#         noOfColumns = len(next(readerData))
#         casesFile.seek(0)
#         headerList = readerData.fieldnames
#         dates = []
#         for col in range(12, noOfColumns):
#             dates.append(headerList[col])
#         confirmedList = []
#         next(readerData) # Skiping the headers row before processsing
#         deathReader = getDeathsReader()
#         next(deathReader) # Skiping the headers row before processsing
#         for row in readerData:
#             for date in dates:
#                 totalCases = 0
#                 totalDeaths = 0
#                 for casesItem in readerData:
#                     totalCases = totalCases + int(casesItem[date])
#                 for deathItem in deathReader:
#                     totalDeaths = totalDeaths + int(deathItem[date])
#                 confirmedList.append(CSVData(date, row["Admin2"], row["Province_State"], totalCases, totalDeaths))
#         writeCsv(confirmedList)
#         # for lis in confirmedList:
#         #     print(f"{lis.date}, {lis.county}, {lis.state}, {lis.case}, {lis.death}")

#         # print(f"confirmed {confirmedList}")     
#         # print(f"Successfully processed {filename}")


def getSum(date, data):
    # f = ""
    # data = ""
    # if(type == "cases"):
    #     f=casesFile
    #     data = casesReader
    # else:
    #     f=deathsFile   
    #     data = deathsReader
    # f.seek(0)
    # next(data)
    # print(date)
    dataList = list(data)
    total = 0
    for row in dataList:
        # print(row)
        # print(date)
        # print(f" {date} : {row[date]}")
        total = total + int(row[date])
    return total

def writeCsv(datas):
    with open('us_cases_and_deaths.csv', 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=headersColumn)
        writer.writeheader()
        for lis in datas:
            writer.writerow({"date" : lis.date, "county": lis.county, "state": lis.state, "case": lis.case, "death": lis.death})



def setTotalCases(dateList, crList, drList):
    # print(dateList)
    # dateList = list(dates)
    # crList = list(casesReader)
    # print(len(crList))
    # for i in crList:
    #     print(i)
    # drList = list(deathsReader)
    for date in dateList:
        # print(date)
        casesDictionary.add(date , getSum(date, crList))
        deathsDictionary.add(date , getSum(date, drList))
    # print(casesDictionary)
    # print(deathsDictionary)


# parseCSV("us_cases.csv")

start()

casesFile.close()
deathsFile.close()


