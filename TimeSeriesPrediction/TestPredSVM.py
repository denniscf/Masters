__author__ = 'denniscf'

import matplotlib.pyplot as plt
from PredSVM import PredSVM
import numpy as np
import unittest

class TestPredSVM(unittest.TestCase):

    def test_GenerateTrainingDataset(self):
        data = [1, 2, 3, 5, 8, 13, 21]
        pSVM = PredSVM(data, 'rbf', 1, 0.1)
        [trainX, trainY, testX, testY] = pSVM.GenerateTrainingTestDataset(3, 0.5)

        self.assertEquals(len(trainX), 2)
        self.assertEquals(len(trainY), 2)
        self.assertEquals(len(testX), 2)
        self.assertEquals(len(testY), 2)

    def test_GridSearch(self):
        C = 1
        gamma = 0.1
        dataTest = np.sin(np.linspace(-4*3.14, 4*3.14, 100 ))
        svm = PredSVM(dataTest, 'rbf', C , gamma)
        [trainX, trainY, testX, testY] = svm.GenerateTrainingTestDataset(6, 0.5)
        svm.Train()
        svm.Predict(trainX)
        scoreNoGS = svm.CalculateScore()

        svm.GridSearch()
        svm.Predict(trainX)
        scoreGS = svm.CalculateScore()

        self.assertEquals(scoreNoGS <= scoreGS, True)

    def test_Predict(self):
        C = 1
        gamma = 0.1
        dataTest = np.sin(np.linspace(-4*3.14, 4*3.14, 100 ))
        svm = PredSVM(dataTest, 'rbf', C , gamma)
        [trainX, trainY, testX, testY] = svm.GenerateTrainingTestDataset(6, 0.5)
        svm.Train()
        predTrainY = svm.Predict(trainX)

        self.assertEquals(len(predTrainY) == len(trainX), True)

        fig = plt.figure()
        ax = plt.subplot(121)
        ax.plot(predTrainY)
        ax = plt.subplot(122)
        ax.plot(trainY)

        predTestY = svm.Predict(testX)
        fig = plt.figure()
        ax = plt.subplot(121)
        ax.plot(predTestY)
        ax = plt.subplot(122)
        ax.plot(testY)

    def test_GenerateSeries(self):
        C = 8000
        gamma = 0.001
        windowSize = 40
        seriesSize = 100
        dataTest = np.sin(np.linspace(-4*3.14, 4*3.14, seriesSize ))
        svm = PredSVM(dataTest, 'rbf', C , gamma)
        [trainX, trainY, testX, testY] = svm.GenerateTrainingTestDataset(windowSize, 0.5)
        svm.Train()
        svm.GridSearch()

        fig = plt.figure()
        ax = plt.subplot(121)
        ax.plot(dataTest[0:int(seriesSize/2)])
        ax = plt.subplot(122)
        ts = svm.GenerateSeries([dataTest[0:int(seriesSize/2)][-windowSize:]], int(seriesSize/2))
        ax.plot(dataTest[int(seriesSize/2):], color='b')
        ax.plot(ts, color='r')
        plt.show()

if __name__ == '__main__':
    unittest.main()