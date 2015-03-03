__author__ = 'denniscf'

import sklearn as skl
import numpy as np
from sklearn.svm import SVR
import numpy
from sklearn import cross_validation as cv
from sklearn.metrics import confusion_matrix
from sklearn.datasets import load_svmlight_file
from sklearn.grid_search import GridSearchCV
from sklearn import preprocessing

class PredSVM:
    def __init__(self, data, kernel, C, gamma):
        self._data = data
        self._kernel = kernel
        self._C = C
        self._gamma = gamma
        self._model = []
        self._trainedSVM = []
        self._trainX = []
        self._trainY = []
        self._testX = []
        self._testY = []

    def GenerateTrainingTestDataset(self, windowSize, percent):
        dataSize = len(self._data)
        x = []
        y = []
        for i in range(windowSize, dataSize):
            x.append(self._data[i - windowSize:i])
            y.append(self._data[i])
        [self._trainX, self._testX, self._trainY, self._testY] = cv.train_test_split(x, y, test_size=percent)

        return self._trainX, self._trainY, self._testX, self._testY

    def GenerateTrainingDataset(self, windowSize):
        dataSize = len(self._data)

        for i in range(windowSize, dataSize):
            self._trainX.append(self._data[i - windowSize:i])
            self._trainY.append(self._data[i])

    #Gamma means how far the influence of a single training example reaches. The lower the value, the bigger the impact
    #A low C makes the decision surface smooth
    def Train(self):
        #svrRBF = SVR(kernel='linear', C=1e5, gamma=1e5) #rbf
        self._model = SVR(kernel=self._kernel, C=self._C, gamma=self._gamma) #rbf
        self._trainedSVM = self._model.fit(self._trainX, self._trainY)

    def GenerateSeries(self, x, nPred):
        y = np.zeros(nPred)
        xAux = []
        xAux.append(x[0])
        for i in range(0, nPred):
            y[i] = self._trainedSVM.predict(xAux[i])
            if i+1 < nPred:
                xAux.append(np.concatenate([xAux[i][1:len(x[0])],[y[i]]]))
        return y

    def Predict(self, x):
        datasetSz = len(x)
        y = np.zeros(datasetSz)
        for i in range(0, datasetSz):
            y[i] = self._trainedSVM.predict(x[i])
        return y

    def PredictTestX(self):
        datasetSz = len(self._testX)
        y = np.zeros(datasetSz)
        for i in range(0, datasetSz):
            y[i] = self._trainedSVM.predict(self._testX[i])
        return y

    def PredictNextN(self, n):
        y = np.zeros(n)
        xAux = []
        xAux.append(self._trainX[-1])
        for i in range(0, n):
            y[i] = self._trainedSVM.predict(xAux[i])
            if i+1 < n:
                xAux.append(np.concatenate([xAux[i][1:len(self._trainX[0])],[y[i]]]))
        return y

    def GridSearch(self):
        # define range dos parametros
        cRange = 2. ** numpy.arange(-5,15,2)
        gammaRange = 2. ** numpy.arange(-15,3,2)

        #k = ['linear', 'rbf']
        paramGrid = dict(gamma=gammaRange, C=cRange, kernel=['linear', 'rbf'])

        srv = SVR(probability=True)

        grid = GridSearchCV(srv, paramGrid, n_jobs=-1, verbose=True)
        grid.fit(self._trainX, self._trainY)

        model = grid.best_estimator_
        self._model = model
        self._trainedSVM = model.fit(self._trainX, self._trainY)

        print('Model was set to best estimator!')
        print(grid.best_params_)

        return model

    def CalculateScore(self):
        self._model.fit(self._trainX, self._trainY)
        return self._model.score(self._testX, self._testY)
