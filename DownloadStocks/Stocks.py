__author__ = 'DCFURLA'

import pandas as pds
from pandas.io.data import DataReader

class Stocks:
    def __init__(self, stocksNames):
        self._names = stocksNames
        self._columns = []
        self._data = []

    def DownloadStocks(self, startingDate, endDate):
        for stock in self._names:
            print("Getting data from {0}...".format(stock))
            stockData = DataReader(stock, "google", startingDate, endDate)
            self._columns = stockData.columns
            print("    Number of lines:{0}".format(stockData.shape[0]))
            self._data.append(stockData)
        return self._data

    def OutputDataToCsv(self):
        init = False
        dataFrame = []
        for column in self._columns:
            for stock in self._names:
                data = self._data[self._names.index(stock)][column]
                if not init:
                    dataFrame = pds.DataFrame(data)
                    dataFrame=dataFrame.rename(columns = {column:stock})
                    init = True
                else:
                    dataFrame[stock] = pds.DataFrame(data)
            dataFrame.to_csv('{0}_Values.csv'.format(column))