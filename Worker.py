import urllib.request
import csv
from datetime import datetime

MONTH_TO_IGNORE = ["January", "February"]

CALIFORNIA_COUNTIES_TO_IGNORE = ["San Diego", "Los Angeles", "Orange"]

deathFileUrl = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_US.csv"
confirmedFileUrl = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_US.csv"
deathFileName = "deaths-us.csv"
confirmedFileName = "confirmed-us.csv"

"""
This method downloads the csv files from given url and also saves the file with the given name.
"""


def download_csv(url, filename):
    print(f"Downloading {filename}")
    urllib.request.urlretrieve(url, filename)
    print(f"{filename} Download success!")


"""
CAll this method to request download
"""


def download_request():
    print("Requesting to download updated file")

    download_csv(confirmedFileUrl, confirmedFileName)
    download_csv(deathFileUrl, deathFileName)

    print("All files downloaded successfully.")


# Requesting to download csv files for further processing.
download_request()

# Opening the files
casesFile = open(confirmedFileName)
deathsFile = open(deathFileName)

# Reading the files
casesReader = csv.DictReader(casesFile)
deathsReader = csv.DictReader(deathsFile)

# These are the column headers to keep in newly generated csv files.
headersColumn = ["date", "county", "state", "cases", "deaths"]

"""
The POJO class to store the data for CSV writing.
"""


class CSVData:
    date = ""
    county = ""
    state = ""
    cases = 0
    deaths = 0

    def __init__(self, date, county, state, cases=0, deaths=0):
        self.date = date
        self.county = county
        self.state = state
        self.cases = cases
        self.deaths = deaths


"""
The custom dictionary class for storing the key value pairs.
"""


class DataDictionary(dict):

    # __init__ function 
    def __init__(self):
        self = dict()

        # Function to add key:value

    def add(self, key, value):
        self[key] = value


casesDictionary = DataDictionary()
deathsDictionary = DataDictionary()

"""
Checks whether the date contains January or February
"""


def is_eligible_to_ignore(date):
    date_object = datetime.strptime(date, "%m/%d/%y")
    month = str(date_object.strftime("%B"))
    if month in MONTH_TO_IGNORE:
        return True
    else:
        return False


"""
The main method for actual processing
"""


def start():
    print("Processing files...")

    no_of_columns = len(next(casesReader))
    casesFile.seek(0)  # starts to read from 0th index
    header_list = casesReader.fieldnames
    dates = []
    for col in range(11, no_of_columns):
        date = str(header_list[col])
        if is_eligible_to_ignore(date) is False:
            dates.append(date)

    final_list = []
    next(casesReader)  # Skipping the headers row before processing

    next(deathsReader)  # Skipping the headers row before processing

    list_maker = casesReader
    cr = list(list_maker)

    uids = []
    for case in cr:
        uids.append(case["UID"])
    dr = list(deathsReader)
    date_list = list(dates)
    count = 0
    update_dictionary(uids, cr, dr)
    for uid in uids:
        case = casesDictionary.get(uid, "")
        death = deathsDictionary.get(uid, "")
        for date in date_list:
            try:
                county = case["Admin2"]
                state = case["Province_State"]
                # Ignoring the counties San Diego, Los Angeles and Orange from California
                if not (state == "California" and county in CALIFORNIA_COUNTIES_TO_IGNORE):
                    count += 1
                    final_list.append(
                        CSVData(date, county, state, int(case[date]), int(death[date])))
            except Exception as e:
                print(f"Error: {e}")
    print(f"No of data generated is: {count}")
    write_csv(final_list)


"""
Writes the given data into the CSV file
"""


def write_csv(datas):
    with open('us_cases_and_deaths.csv', 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=headersColumn)
        writer.writeheader()
        for lis in datas:
            writer.writerow(
                {"date": lis.date, "county": lis.county, "state": lis.state, "cases": lis.cases, "deaths": lis.deaths})
        csvfile.close()


"""
Adds the data into dictionary adding UID as a key and the full row as a value.
"""


def update_dictionary(uids, crList, drList):
    for uid in uids:
        for data in crList:
            if uid == data["UID"]:
                casesDictionary.add(uid, data)
        for data in drList:
            if uid == data["UID"]:
                deathsDictionary.add(uid, data)


print("Starting script.")

start()

casesFile.close()
deathsFile.close()

print("Process Completed successfully.")
