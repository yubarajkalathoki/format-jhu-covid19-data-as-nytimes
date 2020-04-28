import urllib.request
import csv

deathFileUrl = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_US.csv"
confirmedFileUrl = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_US.csv"
deathFileName = "deaths-us.csv"
confirmedFileName = "confirmed-us.csv"


def downloadCSV(url, filename):
    print(f"Downloading {filename}")
    urllib.request.urlretrieve(url, filename)
    print(f"{filename} Download success!")

def downloadRequest():
    print("Requesting to download updated file")
    
    downloadCSV(confirmedFileUrl,  confirmedFileName)
    downloadCSV(deathFileUrl,  deathFileName)

    print("All files downloaded successfully.")

downloadRequest()

casesFile = open(confirmedFileName)
deathsFile = open(deathFileName)

casesReader = csv.DictReader(casesFile)
deathsReader = csv.DictReader(deathsFile)

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
    
    print("Processing files...")

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



def getSum(date, data):
    dataList = list(data)
    total = 0
    for row in dataList:
        total = total + int(row[date])
    return total

def writeCsv(datas):
    with open('us_cases_and_deaths.csv', 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=headersColumn)
        writer.writeheader()
        for lis in datas:
            writer.writerow({"date" : lis.date, "county": lis.county, "state": lis.state, "case": lis.case, "death": lis.death})
        csvfile.close()


def setTotalCases(dateList, crList, drList):
    for date in dateList:
        casesDictionary.add(date , getSum(date, crList))
        deathsDictionary.add(date , getSum(date, drList))

print("Starting script.")

start()

casesFile.close()
deathsFile.close()

print("Process Completed successfully.")

