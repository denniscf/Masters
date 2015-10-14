__author__ = 'dennis'
import numpy as np

def MovingAverage(series, n):
    nElems = len(series)
    ma = np.zeros([1, nElems])

    for i in range(n, nElems):
        ma = np.mean(series[i-n:i])
    return ma

def StochasticPctK(closeSeries, highSeries, lowSeries, nDays=3):
    nElems = len(closeSeries)
    k = np.zeros([1, nElems])
    np.norm
    for i in range(nDays, nElems):
        lowestLow = np.min(lowSeries[i - nDays:i])
        highestHigh = np.max(highSeries[i - nDays:i])
        k[i] = (closeSeries[i] - lowestLow)/(highestHigh - lowestLow)
    return k

def LarryWilliamPctR(closeSeries, highSeries, lowSeries, nDays=3):
    nElems = len(closeSeries)
    k = np.zeros([1, nElems])
    np.norm
    for i in range(nDays, nElems):
        k[i] = (closeSeries[i] - lowSeries[nDays])/(highSeries[nDays] - lowSeries[nDays])
    return k

def BollingerBands(series, nDays=10, K=2):
    nElems = len(series)
    bbUpper = np.zeros([1, nElems])
    bbLower = np.zeros([1, nElems])

    for i in range(nDays, nElems):
        avg = np.mean(series[i-nDays:i])
        stdev = np.std(series[i-nDays:i])
        bbUpper[i] = avg + stdev*K
        bbLower[i] = avg - stdev*K
    return bbUpper, bbLower


#Moving Average on K
def StochasticPctD(K=[], n=3):
    if not K:
        K = StochasticPctK()
    return MovingAverage(series=K, n=n)

def StochasticSlowPctD(D=[], n=3):
    if not D:
        D = StochasticPctD(n=n)
    return MovingAverage(series=D, n=n)

def Momentum(closeSeries, idx, delay=4):
    if idx < delay:
        return closeSeries[idx] - closeSeries[0]
    return closeSeries[idx] - closeSeries[delay]

def PriceRateOfChance(closeSeries):
    nElems = len(closeSeries)
    pct = np.zeros([1, nElems])
    for i in xrange(1, nElems):
       pct[i] = 100*pct[i]/pct[i-1]
    return pct

def AccumDistOscilator(highSeries, lowSeries, closeSeries):
    return (highSeries - closeSeries)/(highSeries - lowSeries)

def DisparityNDays(closeSeries, n=5):
    nElems = len(closeSeries)
    dispNDays = np.zeros([1, nElems])
    for i in xrange(n, nElems):
       dispNDays[n] = closeSeries[i]/np.mean(closeSeries[i-n:i])
    return dispNDays

def PriceOscillator(priceSeries, nMAFast=5, nMASlow=10):
    nElems = len(priceSeries)
    priceOscillator = np.zeros([1, nElems])
    for i in range(nMASlow, nElems):
        valMASlow = np.mean(priceSeries[i-nMASlow:i])
        valMAFast = np.mean(priceSeries[i-nMAFast:i])
        priceOscillator[i] = (valMAFast - valMASlow)/valMAFast

def RelativeStrengthIndex(priceSeries):
    nElems = len(priceSeries)
    rsi = np.zeros([1, nElems])

    # above 70 overbought
    # below 30 is oversold
    for i in range(1, nElems):
        priceROC = PriceRateOfChance(priceSeries[0:i])
        meanUpDays = np.mean(priceROC[priceROC > 0])
        meanDownDays = np.mean(priceROC[priceROC <= 0])
        if meanDownDays == 0:
            meanDownDays = 1
        rsi[i] = 100 * (1 - 1/(1 + meanUpDays/meanDownDays))

