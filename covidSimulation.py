import matplotlib.pyplot as plt

def casesAfter(casesBefore, days, rValue, spreadingDuration):
    return casesBefore * rValue ** (days / spreadingDuration)

def casesBefore(casesAfter, days, rValue, spreadingDuration):
    return casesAfter / rValue / days * spreadingDuration

def casesToRValue(casesBefore, casesAfter, spreadingDuration):
    return casesBefore / casesAfter * spreadingDuration

def r0ToR(casesTotal, population, r0Value):
    if casesTotal >= population:
        return 0
    return r0Value * (1 - casesTotal / population)

def actualToTotalCases(totalCasesBefore, newCases):
    return totalCasesBefore + newCases

def testToActualCases(testCases, darkQuotient):
    return testCases * darkQuotient

def simulate(actualCases, r0Value, population, duration, spreadingDuration, daySamples):
    total = actualCases
    casesArr = [0]
    timeBase = [0]
    timeBaseTotal = [0]
    totalArr = [actualCases] 
    for i in range(int(duration / spreadingDuration)):
        rValue = r0ToR(total, population, r0Value)
        print(rValue)
        actualCases = casesAfter(actualCases, daySamples, rValue, spreadingDuration)
        casesArr.append(int(actualCases))
        timeBase.append(i * daySamples)
        timeBaseTotal.append(i * daySamples )
        total += actualCases
        totalArr.append(total)
        
    return [timeBase, casesArr, timeBase, totalArr]


testCases = 10
r0Value = 5.8
population = 80000
spreadingDuration = 4
daySamples = 0.1
darkQuote = 3

actualCases = testCases * darkQuote
rValue = 0
totalCases = 0

values = simulate(actualCases, r0Value, population, 50 / daySamples, spreadingDuration, daySamples)

plt.plot(values[0], values[1], "-b", values[2], values[3], "-r")
plt.show()