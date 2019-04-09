

import scipy.stats as sp
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt
import numpy as np
import csv


FILE = "data.csv"
RA1 = 0.308 / 0.015
RA2 = 0.264 / 0.005

print(RA1)


RV1 = 5000
RV2 = 50000


def readData(file):
    with open(file, newline="") as file:
        reader = csv.reader(file, delimiter=';', dialect='excel')
        tmp = []
        for index, line in enumerate(reader):
            if "#" in line[0]:

                yield tmp
                tmp = []
                continue

            tmp.append(line)


def transform(data):
    """
    Transform 2d array to two 1d lists
    :param 2d-array like
    :return two arrays (mA, V)
    """

    x = []
    y = []

    for i, j in data:
        i = i.replace(",", ".")
        j = j.replace(",", ".")

        # Add two values to list
        x.append(float(i))
        y.append(float(j))

    return x, y


def trendline(X, Y):
    """
    Returns estimated intercept and slope
    :param X;Y: list of values
    :return intercept, slope
    """

    # Scipy.stats, least square method
    slope, intercept, r, s, err = sp.linregress(X, Y)

    return slope, intercept


def fixVoltage(mA, V):
    """ Fix the current drop on oikeavirtakykentä"""

    rv = []
    for a, v in zip(mA, V):
        rv.append(v - RA2 * a * 0.001)
    return rv


def fixCurrent(mA, V):
    """ Fix the votage drop on oikeajännitekytkentä """
    rv = []
    for a, v in zip(mA, V):
        rv.append(a - v / (RV1 * 0.001))

    return rv



# Total of measures on small resistance
srI = [0]
srV = [0]

# Total measures on large resistance
slI = [0, 0, 0]
slV = [0, 0, 0]

# Pieni resistanssi, oikeajännite
srOjV = []
srOjI = []

# Pieni resistanssi, oikeavirta
srOvV = []
srOvI = []

# Suuri resistanssi, oikeajännite
brOjV = []
brOjI = []

# Suuri resistanssi, oikeavirta
brOvV = []
brOvI = []


for n, measures in enumerate(readData(FILE)):

    mA, V = transform(measures)

    # Oikeajännite, pieni R
    if n == 1:

        # Miksi vitussa nämä on väärinpäin?!?!?!
        srOjV = V
        srOjI = mA

        srI += mA
        srV += V

        plt.xlabel("Virta (mA)")
        plt.ylabel("Jännite (V)")
        # initialize subplots

        x = np.linspace(0.5, 5.5, 100)
        slope, intercept = trendline(mA, V)
        plt.ylim(0, 8.5)
        plt.xlim(0, 5.5)

        plt.scatter(mA, V, marker="x")
        plt.plot(x, slope * x + intercept)

    # Oikeavirta, pieni R
    if n == 2:

        srOvV = V
        srOvI = mA

        srI += mA
        srV += V
        x = np.linspace(0.5, 5.5, 100)
        slope, intercept = trendline(mA, V)

        plt.scatter(mA, V, marker="o")
        plt.plot(x, slope * x + intercept, "-.")

        # Draw the trendline

        a, b = trendline(srI, srV)
        plt.plot(x, a * x + b, "--")

        plt.legend(["Oikeajännitesovite", "Oikeavirtasovite", "Sovite", "Oikeajännite", "Oikeavirta"])

        plt.show()

    # Oikeajännite, suuri R
    if n == 3:

        brOjV = V
        brOjI = mA

        slI += mA
        slV += V

        plt.xlabel("Virta (mA)")
        plt.ylabel("Jännite (V)")

        x = np.linspace(0, 30, 100)

        # calculating trendline
        slope, intercept = trendline(mA, V)

        # Drawing first scatter
        plt.scatter(mA, V, marker="x")

        # drawing it's trendline
        plt.plot(x, slope * x + intercept, "-.")

    # Oikeavirta, suuri R
    if n == 4:

        brOvV = V
        brOvI = mA

        slI += mA
        slV += V

        ovV = mA
        ovI = V

        x = np.linspace(0, 30, 100)
        slope, intercept = trendline(mA, V)

        plt.scatter(mA, V, marker="o")
        plt.plot(x, slope * x + intercept)

        # Draw the trendline
        a, b = trendline(slI, slV)
        plt.plot(x, a * x + b, "--")

        plt.legend(["Oikeajännitesovite", "Oikeavirtasovite", "Sovite", "Oikeajännite", "Oikeavirta"])

        plt.show()


# Now just fix the numbers, make new figures and thats it


print(5 / 5000)
