import urllib.request
import csv

deathFileUrl = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_US.csv"
confirmedFileUrl = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_US.csv"
deathFileName = "deaths-us.csv"
confirmedFileName = "confirmed-us.csv"


def download_csv(url, filename):
    print(f"Downloading {filename}")
    urllib.request.urlretrieve(url, filename)
    print(f"{filename} Download success!")

def download_request():
    print("Requesting to download updated file")
    
    download_csv(confirmedFileUrl, confirmedFileName)
    download_csv(deathFileUrl, deathFileName)

    print("All files downloaded successfully.")

# downloadRequest()

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

    no_of_columns = len(next(casesReader))
    casesFile.seek(0) # starts to read from 0th index
    header_list = casesReader.fieldnames
    dates = []
    for col in range(11, no_of_columns):
        dates.append(header_list[col])
    confirmed_list = []
    next(casesReader) # Skipping the headers row before processing

    next(deathsReader) # Skipping the headers row before processing
    
    list_maker = casesReader
    cr = list(list_maker)

    uids = []
    for case in cr:
        uids.append(case["UID"])
    dr = list(deathsReader)
    date_list = list(dates)
    count = 0
    set_total_cases(uids, cr, dr)
    for uid in uids:
        case = casesDictionary.get(uid, "")
        death = deathsDictionary.get(uid, "")
        for date  in date_list:
            count += 1
            try:
                confirmed_list.append(CSVData(date, case["Admin2"], case["Province_State"], int(case[date]), int(death[date])))
            except Exception as e:
                print(f"Error: {e}")
    print(f"No of data generated is: {count}")
    write_csv(confirmed_list)

def write_csv(datas):
    with open('us_cases_and_deaths.csv', 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=headersColumn)
        writer.writeheader()
        for lis in datas:
            writer.writerow({"date" : lis.date, "county": lis.county, "state": lis.state, "case": lis.case, "death": lis.death})
        csvfile.close()

def set_total_cases(uids, crList, drList):
    for uid in uids:   
        for data in crList:
            if uid == data["UID"]:
                casesDictionary.add(uid , data)
        for data in drList:
            if uid == data["UID"]:
                deathsDictionary.add(uid , data)

print("Starting script.")

start()

casesFile.close()
deathsFile.close()

print("Process Completed successfully.")

