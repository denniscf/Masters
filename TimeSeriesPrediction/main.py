__author__ = 'denniscf'

import matplotlib.pyplot as plt
from FeatureExtractor import FeatureExtractor
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

def PlotResults(ts, testY):
    fig = plt.figure()
    ax = plt.subplot(131)
    ax.set_title('Exponential Average')
    ax.plot(ts, color='r')
    ax = plt.subplot(132)
    ax.set_title('SVM Prediction')
    ax.plot(testY, color='g')
    ax = plt.subplot(133)
    ax.set_title('Overlay')
    ax.plot(ts, color='r')
    ax.plot(testY, color='g')
    plt.show()

#http://pandas.pydata.org/pandas-docs/dev/generated/pandas.stats.moments.ewma.html
def ExponentialMovingAverage(df, days):
    centerOfMass = (days - 1)/2
    ema = pd.stats.moments.ewma(df,com=centerOfMass)
    return ema

def TestPredictionUpDown():
    C = 8192
    gamma = 0.0001220703125
    windowSize = 12
    df = ReadCSVPandas('Close_Values.csv')

    fe = FeatureExtractor()
    featureUpDown = fe.ExtractUpDown(df['BVMF:BBDC4'])

    fig = plt.figure()
    ax = plt.subplot(111)
    ax.plot(featureUpDown, color='r')
    ax.plot(df['BVMF:BBDC4'], color='k')
    plt.show()
    ts = np.array(featureUpDown)

    trainingPeriod = windowSize*30
    testingPeriod = 5

    svm = PredSVM(ts[0:trainingPeriod], 'rbf', C , gamma)
    svm.GenerateTrainingDataset(windowSize)
    svm.Train()
    svm.GridSearch()

    testY = svm.PredictNextN(testingPeriod)
    PlotResults(ts[trainingPeriod:trainingPeriod + testingPeriod ], testY)

    plt.show()

def TestPredictionIntensity():
    C = 8192
    gamma = 0.0001220703125
    windowSize = 12
    df = ReadCSVPandas('Close_Values.csv')

    fe = FeatureExtractor()
    feature = fe.ExtractIntensity(df['BVMF:BBDC4'])

    fig = plt.figure()
    ax = plt.subplot(111)
    ax.plot(feature, color='r')
    ax.plot(df['BVMF:BBDC4'], color='k')
    plt.show()
    ts = np.array(feature)

    trainingPeriod = windowSize*30
    testingPeriod = 5

    svm = PredSVM(ts[0:trainingPeriod], 'rbf', C , gamma)
    svm.GenerateTrainingDataset(windowSize)
    svm.Train()
    svm.GridSearch()

    testY = svm.PredictNextN(testingPeriod)
    PlotResults(ts[trainingPeriod:trainingPeriod + testingPeriod ], testY)

    plt.show()

def TestExponentialMovingAverage():
    C = 8192
    gamma = 0.0001220703125
    windowSize = 20
    df = ReadCSVPandas('Close_Values.csv')
    ema = ExponentialMovingAverage(df['BVMF:BBDC4'],6)

    fig = plt.figure()
    ax = plt.subplot(111)
    ax.plot(ema, color='r')
    ax.plot(df['BVMF:BBDC4'], color='k')
    plt.show()
    ts = np.array(ema)

    print("{0} Mean - {1} Std".format(np.mean(ema), np.std(ema)))
    print("{0} Mean - {1} Std".format(np.mean(np.array(df['BVMF:BBDC4'])), np.std(np.array(df['BVMF:BBDC4']))))

    trainingPeriod = windowSize*30
    testingPeriod = 5

    svm = PredSVM(ts[0:trainingPeriod], 'rbf', C , gamma)
    svm.GenerateTrainingDataset(windowSize)
    #svm.GenerateTrainingTestDataset(windowSize, 0.5)
    svm.Train()
    #svm.GridSearch()

    testY = svm.PredictNextN(testingPeriod)
    PlotResults(ts[trainingPeriod:trainingPeriod + testingPeriod ], testY)

    print('Media {0} - Risco {1}'.format(np.mean(testY), np.std(testY)))
    print('Media {0} - Risco {1}'.format(np.mean(ts[trainingPeriod:trainingPeriod + testingPeriod ]),
                                         np.std(ts[trainingPeriod:trainingPeriod + testingPeriod ])))
    plt.show()

if __name__ == '__main__':
    TestPredictionUpDown()