import requests
from bs4 import BeautifulSoup
from datetime import datetime
import re
import matplotlib.pyplot as plt
import numpy as np

# returns the estimated number of vaccinated people at the given date with the given polynomials
def getYValue(x, fit):
    res = 0
    n = len(fit) - 1
    for i in range(n + 1):
        res += fit[i] * x ** (n - i)
    return res

habitantsBern = 1034977

# defines the degree of the extrapolation (2 is recommended)
fitDegree = 2

# defines the url
page = requests.get("https://www.besondere-lage.sites.be.ch/de/start/impfen.html")

# extracts the whole site
soup = BeautifulSoup(page.content, "html.parser")

dates = []
firstDose = []
secondDose = []

# selects all tables at the site
for elem in soup.select("tbody"):

    # selects all columns at the table
    for elem in elem.select("tr"):

        #selects all the entrys at the column
        count = 0
        for elem in elem.select("td"):
            count += 1

            # turns the html code into text
            entry = elem.text

            # selects the second row only
            if count % 3 == 2:
                firstDose.append(int(str.replace(re.findall("\+?\-?\d+'?\d+", entry)[0], "'", "")))     # regular expression is used
            
            # selects the first row only
            elif count%3 == 1:
                date = ""
                pos = 0

                # makes sure to only have the date
                for letter in entry:
                    if pos <= 7:
                        date += letter
                    pos += 1
                
                # turns the value into a datetime type
                date = datetime.strptime(date, "%d.%m.%y").timestamp()
                dates.append(date)


# makes an extrapolation
fit = np.polyfit(dates, firstDose, fitDegree)
print(fit)

# changes the values to change the datetime range for the estimation
datesEstimated = []
for i in range(int(datetime(2021, 1, 12).timestamp()), int(datetime(2021, 9, 1).timestamp()), 3600):
    datesEstimated.append(i)

# calculates the estimated doses with the extrapolation
firstDoseEstimated =[]
for i in datesEstimated:
    firstDoseEstimated.append(getYValue(i, fit))

# makes sure that only the amount of habitants in Bern could be vaccinated
limitCount = 0
for i in firstDoseEstimated:
    if i > habitantsBern:
        firstDoseEstimated[limitCount] = habitantsBern
    limitCount += 1

# formats the dates to yyyy-mm-dd HH:MM:SS format
datesFormated = []
for i in dates:
    datesFormated.append(datetime.fromtimestamp(i))

# formats the dates for the estimation to yyyy-mm-dd HH:MM:SS format
datesEstimatedFormated = []
for i in datesEstimated:
    datesEstimatedFormated.append(datetime.fromtimestamp(i))

print(firstDose)

# makes a normal plot from with the scraped data and the estimated data
plt.plot(datesFormated, firstDose, "ob", datesEstimatedFormated, firstDoseEstimated, "-r")
plt.show()

# prints the estimated date the entred quote is reaced
quoteCount = 0
#vaccinatonQuote = float(input("Desired vaccination quote: "))
vaccinationQuote = 0.82
for i in firstDoseEstimated:
    if i > (habitantsBern * vaccinationQuote):
        print(datesEstimatedFormated[quoteCount])
        break
    quoteCount += 1