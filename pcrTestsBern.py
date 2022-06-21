import requests
from bs4 import BeautifulSoup
from datetime import datetime
import re
import matplotlib.pyplot as plt
from scipy import interpolate
import numpy as np

def getYValue(x, fit, n):
    res = 0
    for i in range(n + 1):
        res += fit[i] * x ** (n - i)
    return res

habitantsBern = 1034977

page = requests.get("https://www.besondere-lage.sites.be.ch/de/start/impfen.html")

soup = BeautifulSoup(page.content, "html.parser")

weeks = []
tests = []
positiveTests = []
positivity = []

tbody = soup.find_all("tbody")[2]
for elem in tbody.select("tr"):
    count = 0
    for elem in elem.select("td"):
        count += 1
        entry = elem.text
        if count % 4 == 1:
            weeks.append(entry)
        elif count % 4 == 2:
            tests.append(int(str.replace(re.findall("\+?\-?\d+'?\d+", entry)[0], "'", "")))
        elif count % 4 == 3:
            positiveTests.append(int(str.replace(re.findall("\+?\-?\d+'?\d+", entry)[0], "'", "")))
            

#fitDegree = int(input("Type the fit degree: "))

#fit = np.polyfit(weeks, positiveTests, fitDegree)

#print(fit)


plt.plot(weeks, positiveTests, "-", weeks, positivity, "-")
plt.show()