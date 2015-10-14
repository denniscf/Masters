__author__ = 'dennis'
import numpy as np
import math as m

def MovingAverage(series, nDays):
    nElems = len(series)
    ma = np.zeros([nElems])
    startRange = nDays - 1

    for i in xrange(startRange, nElems):
        ma[i] = np.mean(series[i-startRange:i+1])

    return ma

def EMA(series, nDays=3):
    smoothingFactor = 1.0/m.e
    nElems = len(series)
    ema = np.zeros([nElems])
    startRange = nDays - 1

    firstExpDecaySum = 0
    for i in xrange(0, nDays):
        firstExpDecaySum += smoothingFactor*pow((1-smoothingFactor), nDays - i - 1)*series[i]

    ema[startRange] = firstExpDecaySum
    for i in xrange(nDays, nElems):
        ema[i] = smoothingFactor*series[i] + ema[i-1]*(1-smoothingFactor)
    return ema

def WilderSMMA(series, nDays=14):
    smoothingFactor = 1.0/(nDays)
    nElems = len(series)
    ema = np.zeros([nElems])
    startRange = nDays - 1

    smoothingFactors = np.zeros([nDays])
    firstExpDecaySum = 0
    for i in xrange(0, nDays):
        smooth = pow((1-smoothingFactor), nDays - i - 1)
        smoothingFactors[i] = smooth
        firstExpDecaySum += smooth*series[i]
    firstExpDecaySum = smoothingFactor*firstExpDecaySum

    ema[startRange] = firstExpDecaySum
    for i in xrange(nDays, nElems):
        ema[i] = smoothingFactor*series[i] + ema[i-1]*(1-smoothingFactor)

    return ema

def StochasticPctK(closeSeries, highSeries, lowSeries, nDays=3):
    nElems = len(closeSeries)
    pctK = np.zeros([nElems])
    startRange = nDays - 1

    for i in xrange(startRange, nElems):
        lowestLow = np.min(lowSeries[i - startRange:i+1])
        highestHigh = np.max(highSeries[i - startRange:i+1])
        pctK[i] = (closeSeries[i] - lowestLow)/(highestHigh - lowestLow) * 100

    return pctK


#In technical analysis, this is a momentum indicator measuring overbought and oversold levels, similar to a stochastic oscillator.
#It was developed by Larry Williams and compares a stock's close to the high-low range over a certain period of time, usually 14 days.

def WilliamsPctR(closeSeries, highSeries, lowSeries, nDays=3):
    nElems = len(closeSeries)
    pctR = np.zeros([nElems])
    startRange = nDays - 1

    for i in range(startRange, nElems):
        lowestLow = np.min(lowSeries[i - startRange:i+1])
        highestHigh = np.max(highSeries[i - startRange:i+1])
        pctR[i] = (highestHigh - closeSeries[i])/(highestHigh - lowestLow)*(-100)

    return pctR

def BollingerBands(series, nDays=3, K=2):
    nElems = len(series)
    bbUpper = np.zeros([nElems])
    bbLower = np.zeros([nElems])
    startRange = nDays - 1

    for i in range(startRange, nElems):
        avg = np.mean(series[i-startRange:i+1])
        stdev = np.std(series[i-startRange:i+1])
        bbUpper[i] = avg + stdev*K
        bbLower[i] = avg - stdev*K

    return bbUpper, bbLower

#Moving Average on K
def StochasticPctD(K=[], n=3):
    if not K:
        K = StochasticPctK()
    return MovingAverage(series=K, nDays=n)

def StochasticSlowPctD(D=[], n=3):
    if not D:
        D = StochasticPctD(n=n)

    return MovingAverage(series=D, nDays=n)

def Momentum(closeSeries, idx, delay=4):
    if idx < delay:
        return closeSeries[idx] - closeSeries[0]

    return closeSeries[idx] - closeSeries[delay]

def PriceRateOfChange(closeSeries):
    nElems = len(closeSeries)
    pct = np.zeros([nElems])
    for i in xrange(1, nElems):
       pct[i] = float(closeSeries[i] - closeSeries[i-1])/closeSeries[i-1]

    return pct

def AccumDistOscillator(closeSeries, highSeries, lowSeries, volumeSeries):
    adOscillator = ((closeSeries-lowSeries) - (highSeries - closeSeries)) / (highSeries - lowSeries) * volumeSeries

    return adOscillator

def DisparityNDays(closeSeries, n=5):
    nElems = len(closeSeries)
    dispNDays = np.zeros([nElems])
    for i in xrange(n, nElems):
       dispNDays[n] = closeSeries[i]/np.mean(closeSeries[i-n:i])

    return dispNDays

def PriceOscillator(priceSeries, nMAFast=5, nMASlow=10):
    nElems = len(priceSeries)
    priceOscillator = np.zeros([nElems])
    startRangeSlow = nMASlow - 1
    startRangeFast = nMAFast - 1

    for i in range(startRangeSlow, nElems):
        valMASlow = np.mean(priceSeries[i-startRangeSlow:i+1])
        valMAFast = np.mean(priceSeries[i-startRangeFast:i+1])
        priceOscillator[i] = (valMAFast - valMASlow)/valMAFast

    return priceOscillator

def RelativeStrengthIndex(priceSeries, nDays=14):
    nElems = len(priceSeries)
    rsi = np.zeros([nElems])
    rs = np.zeros([nElems])

    # above 70 > overbought
    # below 30 > oversold
    startRange = nDays - 1
    priceAbsChange = np.zeros([nElems])
    priceAbsChange[1:] = priceSeries[1:] - priceSeries[0:-1]

    for i in xrange(startRange, nElems):
        priceAbsChangeInterval = priceAbsChange[i-startRange:i+1]
        upDays = np.abs(priceAbsChangeInterval * (priceAbsChangeInterval > 0))
        downDays = np.abs(priceAbsChangeInterval * (priceAbsChangeInterval < 0))
        upDaysSMMA = WilderSMMA(series=upDays, nDays=14)
        downDaysSMMA = WilderSMMA(series=downDays, nDays=14)
        if upDaysSMMA[-1] == 0:
            u = 1
        else:
            u = abs(upDaysSMMA[-1])

        if downDaysSMMA[-1] == 0:
            d = 1
        else:
            d = abs(downDaysSMMA[-1])

        rs[i] = u/d
        rsi[i] = 100 - 100/(1 + rs[i])

    return rsi