import scipy.stats as sp
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt
import numpy as np
import csv

REPO = "https://github.com/pyyttoni/sahkomittaukset.git"


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


def func(x, a, b, c):
    return a * np.exp(-b * x) + c


def exponentialTrendline(X, Y):
    """
    Returns estimated coefficients for exponential graph
    :param X,Y: list of values
    :return coefficients for exponential curve
    """

    popt, pcov = curve_fit(func, X, Y)
    # This function may not work because the values are quite small
    # and they are close to their max dtype (float64 or float32)
    # In this case warning can be ignored

    return popt


def main():
    FILE = 'jannite.csv'
    LAMPPU = "hehkulamppu.csv"

    # First draw two graphs, oikeajännite ja oikeavirta

    fig, axs = plt.subplots(2, 1, constrained_layout=True)
    # Get data
    for n, measures in enumerate(readData(FILE)):

        mA, V = transform(measures)

        # Oikeajännite, pieni R
        if n == 1:
            # initialize subplots

            x = np.linspace(3, 5.5, 100)
            slope, intercept = trendline(mA, V)

            axs[0].scatter(mA, V)
            axs[0].plot(x, slope * x + intercept)

        # Oikeavirta, pieni R
        if n == 2:
            x = np.linspace(3, 5.5, 100)
            slope, intercept = trendline(mA, V)

            axs[0].scatter(mA, V)
            axs[0].plot(x, slope * x + intercept)
            axs[0].legend(["Oikeajannite, pieni resistanssi", "Oikeajannite, trendline", "Oikeavirta, pieni resistanssi", "Oikeavirta, trendline"])

            fig.suptitle("Vastuksen resistanssit")

        # Oikeajännite, suuri R
        if n == 3:
            x = np.linspace(15, 30, 100)
            slope, intercept = trendline(mA, V)
            axs[1].scatter(mA, V)
            axs[1].plot(x, slope * x + intercept)

        # Oikeavirta, suuri R
        if n == 4:
            x = np.linspace(15, 30, 100)
            slope, intercept = trendline(mA, V)

            axs[1].scatter(mA, V)
            axs[1].plot(x, slope * x + intercept)
            axs[1].legend(["Oikeajannite, suuri resistanssi", "Oikeajannite, sovite", "Oikeavirta, suuri resistanssi", "Oikeavirta, sovite"])

            plt.show()

    # Get lamp-data
    fig2, axs2 = plt.subplots(1, 2, constrained_layout=True)
    for n, measurements in enumerate(readData(LAMPPU)):

        mA, V = transform(measurements)
        if n == 1:

            # Oikeajännite
            x = np.linspace(0, 21, 100)
            popt = exponentialTrendline(mA, V)
            print(popt)
            axs2[0].scatter(mA, V)
            axs2[0].plot(x, func(x, *popt), "b-")

        if n == 2:
            # Oikeavirta
            popt = exponentialTrendline(mA, V)
            axs2[1].scatter(mA, V)
            axs2[1].plot(x, func(x, *popt), 'r-')

            plt.show()

        # Draw the lamp graphs


main()
