__author__ = 'denniscf'

import unittest
import FinancialFeatures as ff
import numpy as np
import matplotlib.pyplot as plt


class FinancialFeaturesTest(unittest.TestCase):
    # Tested - OK
    def testMovingAverage(self):
        series = np.array([1, 2, 3, 4, 5, 6])
        maExpectedResult = np.array([0, 0, 6 / 3, 9 / 3, 12 / 3, 15 / 3])
        ma = ff.MovingAverage(series=series, nDays=3)

        self.failUnless(np.all(maExpectedResult == ma))

    # Tested - OK
    def testWilliamsPctR(self):
        close = np.array([1, 2, 1.5, 2.5, 3])
        highs = np.array([1.3, 2.3, 1.8, 2.8, 3.3])
        lows = np.array([0.7, 1.8, 1.2, 2.2, 2.7])
        lw = ff.WilliamsPctR(close, highs, lows, nDays=3)
        lwExpectedResult = np.array([0, 0, -50, -18.75, -14.285714])
        self.failUnless(np.allclose(lw, lwExpectedResult))

        fig = plt.figure()
        plt.subplot(211)
        plt.plot(highs, color='r')
        plt.plot(close, color='g')
        plt.plot(lows, color='b')
        plt.subplot(212)
        plt.plot(lw, color='k')
        plt.title('William %R')
        plt.show()


    def testStochasticPctK(self):
        close = np.array([1, 2, 1.5, 2.5, 3])
        highs = np.array([1.3, 2.3, 1.8, 2.8, 3.3])
        lows = np.array([0.7, 1.8, 1.2, 2.2, 2.7])
        pctK = ff.StochasticPctK(close, highs, lows, nDays=3)
        pctKExpectedResult = np.array([0, 0, 50, 81.25, 85.714286])
        print(pctK)

        self.failUnless(np.allclose(pctK, pctKExpectedResult))
        fig = plt.figure()
        plt.subplot(211)
        plt.plot(highs, color='r')
        plt.plot(close, color='g')
        plt.plot(lows, color='b')
        plt.subplot(212)
        plt.plot(pctK, color='k')
        plt.title('Stochastic %K')
        plt.show()


    # Tested - OK
    def testBollingerBands(self):
        close = np.array([1, 2, 1.5, 2.5, 3, -1, 1])
        [bbUp, bbDown] = ff.BollingerBands(close, nDays=3, K=2)
        expectedBBUp = np.array([0, 0, 2.31649658, 2.81649658, 3.58055246, 5.05902608,  4.26598632])
        expectedBBDown = np.array([0, 0, 0.68350342, 1.18350342, 1.0861142, -2.05902608, -2.26598632])
        self.failUnless(np.allclose(bbUp, expectedBBUp))
        self.failUnless(np.allclose(bbDown, expectedBBDown))

        fig = plt.figure()
        plt.title('Bollinger Bands')
        ax = fig.add_subplot(111)
        ax.plot(close, color='k')
        ax.plot(bbUp, color='g')
        ax.plot(bbDown, color='r')
        plt.show()

    # Tested - OK
    def testPriceRateOfChance(self):
        close = np.array([1, 2, 5, 3, 1, 3, 1])
        pct = ff.PriceRateOfChange(close)
        pctExpected = np.array([0, 1, 1.5, -0.4, -0.66666667, 2, -0.66666667])
        self.failUnless(np.allclose(pct, pctExpected))

    # Tested - OK
    def testPriceOscillator(self):
        close = np.array([1, 2, 1.5, 2.5, 3, -1, 1, 4, 3, 5, 1])
        priceOscillation = ff.PriceOscillator(close, nMAFast=3, nMASlow=5)
        priceOscillationExpected = np.array([0, 0, 0, 0, 14.285714, -6.666667, -40, -42.5, 25, 40, 6.666667])
        self.failUnless(np.allclose(priceOscillation, priceOscillationExpected))

        fig = plt.figure()
        plt.title('Price Oscillator')
        ax = fig.add_subplot(111)
        ax.plot(close, color='r')
        ax.plot(priceOscillation, color='k')
        plt.show()

    # Tested - Ok
    def testRelativeStrengthIndex(self):
        close = np.array(
            [44.34, 44.09, 44.15, 43.61, 44.33, 44.83, 45.10, 45.42, 45.84, 46.08, 45.89, 46.03, 45.61, 46.28,
             46.28, 46.00, 46.03, 46.41, 46.22, 45.64, 46.21, 46.25, 45.71, 46.45, 45.78, 45.35, 44.03, 44.18,
             44.22, 44.57, 43.42, 42.66, 43.13])
        rsi = ff.RelativeStrengthIndex(close, nDays=14)
        rsiExpected = np.array([1, 2, 1.5, 2.5, 3, -1, 1, 4, 3, 5, 1])

        fig = plt.figure(1)
        plt.title('RSI')
        ax = fig.add_subplot(111)

        ax.plot(close, color='k')
        ax.plot(rsi, color='g')
        plt.show()

        #self.failUnless(np.allclose(rsi, rsiExpected))

    # Tested - Ok
    def testExponentialMovingAverage(self):
        close = np.array(
            [44.34, 44.09, 44.15, 43.61, 44.33, 44.83, 45.10, 45.42, 45.84, 46.08, 45.89, 46.03, 45.61, 46.28, 46.28,
             46.00, 46.03, 46.41, 46.22, 45.64, 46.21, 46.25, 45.71, 46.45, 45.78, 45.35, 44.03, 44.18, 44.22, 44.57,
             43.42, 42.66, 43.13])
        ema = ff.EMA(close, nDays=14)

        fig = plt.figure(1)
        plt.title('Exponential Moving Average')
        ax = fig.add_subplot(111)
        ax.plot(close, color='k')
        ax.plot(ema, color='g')
        plt.show()

    # Tested - Ok
    def testWilderSMMA(self):
        close = np.array(
            [44.34, 44.09, 44.15, 43.61, 44.33, 44.83, 45.10, 45.42, 45.84, 46.08, 45.89, 46.03, 45.61, 46.28, 46.28,
             46.00, 46.03, 46.41, 46.22, 45.64, 46.21, 46.25, 45.71, 46.45, 45.78, 45.35, 44.03, 44.18, 44.22, 44.57,
             43.42, 42.66, 43.13])
        ema = ff.WilderSMMA(close, nDays=14)

        fig = plt.figure(1)
        plt.title('Wilder SMMA')
        ax = fig.add_subplot(111)
        ax.plot(close, color='k')
        ax.plot(ema, color='g')
        plt.show()

    def testMomentum(self):
        closeSeries = np.array([0, 1, 2, 3, 4, 2, 3.0, 1, 5.5, 6])
        expectedMomentum = np.array([-999, -999, -999, -999, 4, 1, 1, -2, 1.5, 4])
        momentum = ff.Momentum(closeSeries, delay=4)
        self.failUnless(np.allclose(momentum, expectedMomentum))

if __name__ == '__main__':
    unittest.main()
