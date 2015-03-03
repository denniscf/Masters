__author__ = 'denniscf'

import matplotlib.pyplot as plt
from PredSVM import PredSVM


import csv
import numpy as np
import pandas as pd

def ReadCSV(filePath):
    file = csv.reader(open(filePath))
    for r in file:
        header = r
        break

    ds = np.genfromtxt(filePath, dtype=None, delimiter=",", skiprows=1)
    return header, ds

def ReadCSVPandas(filePath):
    df = pd.DataFrame(pd.read_csv(filePath))
    return df

def TestSVMPrediction():
    C = 0.1
    gamma = 0.1
    windowSize = 6
    df = ReadCSVPandas('Close_Values.csv')
    ts = np.array(df['BVMF:BBDC4'])
    trainingPeriod = windowSize*40
    testingPeriod = 6

    svm = PredSVM(ts[0:trainingPeriod], 'rbf', C, gamma)
    svm.GenerateTrainingDataset(windowSize)
    svm.Train()
    svm.GridSearch()

    testY = svm.PredictNextN(testingPeriod)

    fig = plt.figure()
    ax = plt.subplot(121)
    ax.plot(ts[trainingPeriod + 1:trainingPeriod + 1 + testingPeriod], color='r')
    ax = plt.subplot(122)
    ax.plot(testY, color='b')
    plt.show()

def TestSVMPredictionAccuracy():
    C = 0.1
    gamma = 0.1
    windowSize = 6
    df = ReadCSVPandas('Close_Values.csv')
    ts = np.array(df['BVMF:BBDC4'])

    svm = PredSVM(ts[0:100], 'rbf', C, gamma)
    svm.GenerateTrainingTestDataset(windowSize, 0.5)
    svm.Train()
    svm.GridSearch()
    testY = svm.PredictTestX()

    fig = plt.figure()
    ax = plt.subplot(131)
    plt.title('True values')
    ax.plot(svm._testY, color='r')
    ax = plt.subplot(132)
    plt.title('Predicted values')
    ax.plot(testY, color='b')
    ax = plt.subplot(133)
    plt.title('Error')
    ax.plot(svm._testY - testY, color='b')
    plt.show()

if __name__ == '__main__':
    TestSVMPredictionAccuracy()