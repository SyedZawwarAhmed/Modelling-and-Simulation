import math
import random
from decimal import *
from texttable import Texttable

def getArrivalTimes(meanArrivalNumber):
    cumulativeProbability = 0
    cumulativeProbabilities = []
    x = 0
    while cumulativeProbability < 1.0:
        with localcontext() as ctx:
            ctx.prec = 5
            newValue = (Decimal(math.exp(-meanArrivalNumber))*ctx.power(Decimal(meanArrivalNumber),x)) / math.factorial(x)
            cumulativeProbability += newValue
            cumulativeProbabilities.append(float(cumulativeProbability))
        x += 1

    cpLookUp = [0]
    for i in range(len(cumulativeProbabilities) - 1):
        cpLookUp.append(cumulativeProbabilities[i])

    averageTimes = [i for i in range(len(cumulativeProbabilities))]

    interArrivals = []
    for i in range(len(cumulativeProbabilities)):
        randomNumber = random.random()
        for j in range(len(cumulativeProbabilities)):
            item = cumulativeProbabilities[j]
            if randomNumber < item:
                interArrivals.append(j)
                break

    arrivalTimes = [interArrivals[0]]
    for i in range(1, len(interArrivals)):
        arrivalTimes.append(arrivalTimes[i - 1] + interArrivals[i])
    return {
        "cumulativeProbabilities": cumulativeProbabilities,
        "cpLookUp": cpLookUp,
        "averageTimes": averageTimes,
        "interArrivals": interArrivals,
        "arrivalTimes": arrivalTimes
    }
    

def getServiceTimes(length, meanServiceNumber):
    serviceTimes = []
    for i in range(length):
        serviceTime = -meanServiceNumber * math.log(random.random())
        serviceTimes.append(round(serviceTime))
    return serviceTimes

def getPriorities(length, A, M, Z, C, a, b):
    priorities = []
    for i in range(length):
        R = (A * Z + C) % M
        S = R / M
        Y = round((b - a) * S + a)
        priorities.append(Y)
        Z = R
    return priorities

def display(arrivalTimes, serviceTimes, priorities):
    table = Texttable()
    table.set_precision(5)
    tableRows = [["S. No.", "Cumulative Probabilities", "CP Lookup", "Average Times", "Inter Arrivals", "Arrival Times", "Service Times", "Priorities"]]
    for i in range((len(arrivalTimes['arrivalTimes']))):
        newRow = [
            i+1, 
            arrivalTimes["cumulativeProbabilities"][i],
            arrivalTimes["cpLookUp"][i],
            arrivalTimes["averageTimes"][i],
            arrivalTimes["interArrivals"][i],
            arrivalTimes["arrivalTimes"][i],
            serviceTimes[i],
            priorities[i]
        ]
        tableRows.append(newRow)
    table.add_rows(tableRows)
    table.set_max_width(200)
    print(table.draw())
    

if __name__ == "__main__":
    # meanArrivalNumber = 2.25
    # meanServiceNumber = 8.98
    # A = 55
    # M = 1994
    # Z = 10112166
    # C = 9
    # a = 1
    # b = 3
    meanArrivalNumber = float(input("Enter the value of Mean Arrival Number:- "))
    meanServiceNumber = float(input("Enter the value of Mean Service Number:- "))
    A = int(input("Enter the value of A:- "))
    M = int(input("Enter the value of M:- "))
    Z = int(input("Enter the value of Z:- "))
    C = int(input("Enter the value of C:- "))
    a = int(input("Enter the value of a:- "))
    b = int(input("Enter the value of b:- "))


    arrivalTimes = getArrivalTimes(meanArrivalNumber)
    serviceTimes = getServiceTimes(len(arrivalTimes['arrivalTimes']), meanServiceNumber)
    priorities = getPriorities(len(arrivalTimes['arrivalTimes']), A, M, Z, C, a, b)
    display(arrivalTimes, serviceTimes, priorities)
